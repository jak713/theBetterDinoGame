from sys import exit

import pygame

from constants import (
    FONT,
    FPS,
    SCORE_MULTIPLIER,
    SCREEN_SIZE,
    PLAYER_TEXT_FONT_SIZE,
    SKY,
    GROUND,
    GROUND_SIZE,
    BACKGROUND_COLOUR,
    GROUND_COLOUR
)
from gamestate import GameState
from obstaclefield import ObstacleField
from player import Player
from gamerun import GameRun
from local_scores import get_top_score
from displayfunctions import display_score, leaderboard, game_over, title_screen

from api_client import (
    create_player_api_client,
    create_game_run_api_client,
    update_game_run_api_client,    
    delete_game_run_api_client
)

def clean_username(username: str) -> str:
    username = username.strip()
    return username if username else "player1"

def load_sound() -> tuple[pygame.mixer.Sound, pygame.mixer.Sound]:
    """
    Looks for audio files if present, returns pygame Sounds as jump_fx, game_over_fx. 
    Otherwise returns pygame Sounds silent, silent.
    """
    try:
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
        return jump_fx, game_over_fx

    except (FileNotFoundError, pygame.error) as e:
        print(f"Audio files not found! Resorting to silence... Details: {e}")
        silent = pygame.mixer.Sound(buffer=bytes(44))
        return silent, silent

def load_background(screen: pygame.Surface) -> tuple[pygame.Surface, pygame.Surface, pygame.Rect]:
    """
    Looks for asset files if present, returns (background:Surface, ground:Surface, ground_rect:Rect)
    Otherwise returns block colours in the same way.
    """
    try:
        background = pygame.image.load(SKY).convert()
        background = pygame.transform.smoothscale(background, screen.get_size())

        ground = pygame.image.load(GROUND).convert_alpha()
        ground = pygame.transform.smoothscale(ground, GROUND_SIZE)
        ground_rect = ground.get_rect(bottomleft=(0, 400))
        return background, ground, ground_rect

    except (FileNotFoundError, pygame.error) as e:
        print(f"Assets not found! Resorting to colours... Error details: {e}")
        background = pygame.Surface(SCREEN_SIZE)
        background.fill(BACKGROUND_COLOUR)

        ground = pygame.Surface(GROUND_SIZE)
        ground_rect = ground.get_rect(bottomleft=(0, 400))
        ground.fill(GROUND_COLOUR)
        return background, ground, ground_rect

def main() -> None:
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    background, ground, ground_rect = load_background(screen)
    jump_fx, game_over_fx = load_sound()

    pygame.display.set_caption("Dino Game")

    clock = pygame.time.Clock()
    fps = FPS
    dt = 0
    
    player = pygame.sprite.GroupSingle()
    text_font = pygame.font.SysFont(FONT, PLAYER_TEXT_FONT_SIZE)
    obstacles = pygame.sprite.Group()
    field = ObstacleField(obstacles)

    game_state = GameState.TITLE # Essentially keeps track of the screen
    
    run = None # Keeps track of the run
    last_game_run_id = None
    delete_message_time = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_state == GameState.TITLE:
                game_state, username = title_screen(screen, last_game_run_id, delete_message_time)
                if game_state == GameState.NEWGAME:
                    # starts the obstacles from the beginning/fresh
                    obstacles.empty()
                    player.empty()

                    cleaned_username = clean_username(username)
                    try:
                        player_response = create_player_api_client(cleaned_username)
                        game_run_response = create_game_run_api_client(player_response["player_id"])
                    except Exception as e:
                        print(f"Server not found. Switching to offline... Error details: {e}")
                        player_response = None
                        game_run_response = None

                    run = GameRun(
                        player_id=player_response["player_id"] if player_response else "offline",
                        game_run_id=game_run_response["game_run_id"] if game_run_response else "offline",
                        username=cleaned_username,
                        state = game_state
                    )

                    text_font = pygame.font.SysFont(FONT, PLAYER_TEXT_FONT_SIZE)
                    player.add(Player(text_font, jump_fx,  cleaned_username))


        if game_state == GameState.DELETE_RUN:
            delete_game_run_api_client((last_game_run_id))
            last_game_run_id = None
            delete_message_time = pygame.time.get_ticks()
            game_state = GameState.TITLE

        if game_state == GameState.QUIT:
            pygame.quit()
            return

        if run is not None and run.is_active():
            for o in obstacles:
                if pygame.sprite.collide_mask(player.sprite, o):
                    try:
                        update_game_run_api_client(run.game_run_id, run.final_score())
                    except Exception:
                        pass
                    
                    last_game_run_id = run.game_run_id
                    run.save_to_file()
                    top_three_scores = get_top_score()
                    game_state = game_over(screen, game_over_fx, top_three_scores)
                    run.transition(game_state)

            obstacles.update(dt)
            field.update(dt, run.score)
            player.update()
            run.update_score(dt, SCORE_MULTIPLIER)

            screen.blit(background, (0, 0))
            screen.blit(ground, ground_rect)
            player.draw(screen)
            screen.blit(player.sprite.name, player.sprite.name_rect)
            obstacles.draw(screen)

            display_score(screen, run.score)

            pygame.display.flip()
            time = clock.tick(fps)
            # dt limited to 0.1 during blocked screens (title screen)
            dt = min(time / 1000, 0.1)

        if game_state == GameState.LEADERBOARD:
            game_state = leaderboard(screen)


if __name__ == "__main__":
    main()
