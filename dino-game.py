from sys import exit

import pygame

from api_client import (
    create_player_api_client,
    create_game_run_api_client,
    fetch_leaderboard_api_client,
    update_game_run_api_client,
)


from button import Button
from constants import (
    BACKGROUND_COLOUR,
    BUTTON_FONT_SIZE,
    FONT,
    GROUND_COLOUR,
    GROUND_SIZE,
    PLAYER_USERNAME_BACKGROUND,
    RETURN_MENU_BUTTON_FONT_SIZE,
    SCORE_COORDINATES,
    SCORE_MULTIPLIER,
    SCREEN_SIZE,
    PROMPT_FONT_SIZE,
    SCORE_FONT_SIZE,
    PLAYER_TEXT_FONT_SIZE,
)
from gamestate import GameState
from obstaclefield import ObstacleField
from player import Player


def display_score(screen: pygame.Surface, score: float) -> None:
    font = pygame.font.SysFont(FONT, SCORE_FONT_SIZE)
    score_surface = font.render(f"Score: {int(score)}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(topleft=SCORE_COORDINATES)
    screen.blit(score_surface, score_rect)


def title_screen(screen: pygame.Surface) -> tuple[GameState, str]:
    """
    Accepts screen as argument and renders Start/Quit/Leaderboard buttons to screen.
    Returns GameState or tuple[GameState, str]
        Start -> (GameState.NEWGAME, username_input)
        Quit -> (GameState.QUIT, username_input)
        Leaderboard -> (GameState.LEADERBOARD, username_input)
    """
    start_btn = Button(
        center_position=(400, 200),
        font_size=BUTTON_FONT_SIZE,
        bg_rgb=BACKGROUND_COLOUR,
        text_rgb=GROUND_COLOUR,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = Button(
        center_position=(400, 300),
        font_size=BUTTON_FONT_SIZE,
        bg_rgb=BACKGROUND_COLOUR,
        text_rgb=GROUND_COLOUR,
        text="Quit",
        action=GameState.QUIT,
    )
    leaderboard_btn = Button(
        center_position=(400, 250),
        font_size=BUTTON_FONT_SIZE,
        bg_rgb=BACKGROUND_COLOUR,
        text_rgb=GROUND_COLOUR,
        text="Leaderboard",
        action=GameState.LEADERBOARD,
    )

    username_input = ""
    buttons = [start_btn, quit_btn, leaderboard_btn]
    text_font = pygame.font.SysFont(FONT, 25)
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username_input = username_input[:-1]
                else:
                    username_input += event.unicode

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BACKGROUND_COLOUR)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action, username_input
            button.draw(screen)

        input_rect = pygame.Rect((200, 120), (400, 50))
        pygame.draw.rect(screen, GROUND_COLOUR, input_rect, 2)
        input_surface = text_font.render(username_input, True, GROUND_COLOUR)
        screen.blit(input_surface, input_surface.get_rect(center=(400, 150)))
        pygame.display.flip()


def leaderboard(screen: pygame.Surface) -> GameState:
    return_btn = Button(
        center_position=(200, 370),
        font_size=RETURN_MENU_BUTTON_FONT_SIZE,
        bg_rgb=BACKGROUND_COLOUR,
        text_rgb=GROUND_COLOUR,
        text="Return to main menu",
        action=GameState.TITLE,
    )

    leaderboard_data = fetch_leaderboard_api_client()

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BACKGROUND_COLOUR)

        leaderboard_font = pygame.font.SysFont(FONT, 40)
        leaderboard_message = leaderboard_font.render(
            "Leaderboard", True, GROUND_COLOUR
        )
        leaderboard_message_rect = leaderboard_message.get_rect(center=(400, 20))
        screen.blit(leaderboard_message, leaderboard_message_rect)

        font = pygame.font.SysFont(FONT, 20)
        # Header
        screen.blit(font.render("Rank", True, GROUND_COLOUR), (150, 50))
        screen.blit(font.render("Username", True, GROUND_COLOUR), (300, 50))
        screen.blit(font.render("Score", True, GROUND_COLOUR), (550, 50))

        # Rows
        y = 75
        for rank, (username, score) in enumerate(leaderboard_data, start=1):
            screen.blit(font.render(str(rank), True, GROUND_COLOUR), (150, y))
            screen.blit(font.render(username, True, GROUND_COLOUR), (300, y))
            screen.blit(font.render(str(score), True, GROUND_COLOUR), (550, y))
            y += 29

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(screen)

        pygame.display.flip()


def game_over(screen: pygame.Surface, game_over_fx: pygame.mixer.Sound) -> GameState:
    background = screen.copy()
    font = pygame.font.SysFont(FONT, PROMPT_FONT_SIZE)
    prompt = font.render("PRESS SPACE TO CONTINUE", False, (64, 64, 64))
    game_over_fx.play()
    prompt_rect = prompt.get_rect(center=(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            return GameState.TITLE

        screen.blit(background, (0, 0))
        if pygame.time.get_ticks() // 500 % 2 == 0:  # changes every half a second
            screen.blit(prompt, prompt_rect)
        pygame.display.flip()


def main() -> None:
    pygame.init()
    pygame.font.init()

    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()

    # load sound
    pygame.mixer.music.load("audio/game-music.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1, 0.0, 5000)
    jump_fx = pygame.mixer.Sound("audio/jump.mp3")
    jump_fx.set_volume(0.3)
    game_over_fx = pygame.mixer.Sound("audio/game-over.mp3")
    game_over_fx.set_volume(0.3)

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Dino Game")

    clock = pygame.time.Clock()
    fps = 60
    dt = 0
    
    background = pygame.image.load("assets/sky1.png").convert()
    background = pygame.transform.smoothscale(background, screen.get_size())

    ground = pygame.image.load("assets/3.png").convert_alpha()
    ground = pygame.transform.smoothscale(ground, GROUND_SIZE)
    ground_rect = ground.get_rect(bottomleft=(0, 400))

    player = pygame.sprite.GroupSingle()
    text_font = pygame.font.SysFont(FONT, PLAYER_TEXT_FONT_SIZE)

    obstacles = pygame.sprite.Group()
    field = ObstacleField(obstacles)

    score = 0
    game_state = GameState.TITLE

    username = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if game_state == GameState.TITLE:
            game_state, username = title_screen(screen)
            # resetting the score back to 0 once the starts over again
            if game_state == GameState.NEWGAME:
                score = 0
                # starts the obstacles from the beginning/fresh
                obstacles.empty()
                if not username.strip():
                    username = "player1"

                player_response = create_player_api_client(username)
                player_id = player_response["player_id"]

                game_run_response = create_game_run_api_client(player_id)
                game_run_id = game_run_response["game_run_id"]

                text_font = pygame.font.SysFont(FONT, PLAYER_TEXT_FONT_SIZE)
                player.add(Player(text_font, jump_fx, username))

        if game_state == GameState.QUIT:
            pygame.quit()
            return
        if game_state == GameState.NEWGAME:
            for o in obstacles:
                if pygame.sprite.collide_mask(player.sprite, o):
                    update_game_run_api_client(game_run_id, int(score))
                    game_state = game_over(screen, game_over_fx)

            obstacles.update(dt)
            field.update(dt)
            player.update()
            score += dt * SCORE_MULTIPLIER

            screen.blit(background, (0, 0))
            screen.blit(ground, ground_rect)
            player.draw(screen)
            pygame.draw.rect(
                screen, PLAYER_USERNAME_BACKGROUND, player.sprite.name_rect
            )
            screen.blit(player.sprite.name, player.sprite.name_rect)
            obstacles.draw(screen)

            display_score(screen, score)

            pygame.display.flip()
            time = clock.tick(fps)
            # dt limited to 0.1 during blocked screens (title screen)
            dt = min(time / 1000, 0.1)

        if game_state == GameState.LEADERBOARD:
            game_state = leaderboard(screen)


if __name__ == "__main__":
    main()
