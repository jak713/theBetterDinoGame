import pygame
from constants import (
    FONT,
    SCORE_FONT_SIZE, 
    BUTTON_FONT_SIZE, 
    BACKGROUND_COLOUR, 
    GROUND_COLOUR, 
    RETURN_MENU_BUTTON_FONT_SIZE,
    SCORE_COORDINATES,
    SCREEN_SIZE,
    PROMPT_FONT_SIZE,
    ) 
from button import Button
from gamestate import GameState

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

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BACKGROUND_COLOUR)

        leaderboard_font = pygame.font.SysFont(FONT, 40)
        leaderboard_message = leaderboard_font.render(
            "Leaderboard", False, GROUND_COLOUR
        )
        leaderboard_message_rect = leaderboard_message.get_rect(center=(400, 50))
        screen.blit(leaderboard_message, leaderboard_message_rect)

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

