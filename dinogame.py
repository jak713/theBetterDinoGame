from sys import exit

import pygame

from constants import (
    BACKGROUND_COLOUR,
    FONT,
    FPS,
    GROUND_COLOUR,
    GROUND_SIZE,
    PLAYER_USERNAME_BACKGROUND,
    SCORE_MULTIPLIER,
    SCREEN_SIZE,
    PLAYER_TEXT_FONT_SIZE,
)
from gamestate import GameState
from obstaclefield import ObstacleField
from player import Player
from displayfunctions import display_score, leaderboard, game_over, title_screen


def update_score(score: float, dt: float, multiplier: int) -> float:
    return score + dt * multiplier

def clean_username(username: str) -> str:
    username = username.strip()
    return username if username else "player1"

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
    fps = FPS
    dt = 0

    background = pygame.Surface(SCREEN_SIZE)
    background.fill(BACKGROUND_COLOUR)

    ground = pygame.Surface(GROUND_SIZE)
    ground_rect = ground.get_rect(bottomleft=(0, 400))
    ground.fill(GROUND_COLOUR)

    player = pygame.sprite.GroupSingle()
    obstacles = pygame.sprite.Group()
    field = ObstacleField(obstacles)

    score = 0
    game_state = GameState.TITLE

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

                text_font = pygame.font.SysFont(FONT, PLAYER_TEXT_FONT_SIZE)
                cleaned_username = clean_username(username)
                player.add(Player(text_font, jump_fx,  cleaned_username))

        if game_state == GameState.QUIT:
            pygame.quit()
            return

        if game_state == GameState.NEWGAME:
            for o in obstacles:
                if o.rect.colliderect(player.sprite.rect):
                    game_state = game_over(screen, game_over_fx)

            obstacles.update(dt)
            field.update(dt)
            player.update()
            score = update_score(score, dt, SCORE_MULTIPLIER)

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
