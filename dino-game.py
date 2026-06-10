from sys import exit

import pygame

from button import Button
from constants import (
    BACKGROUND_COLOUR,
    FONT,
    GROUND_COLOUR,
    GROUND_SIZE,
    PLAYER_USERNAME_BACKGROUND,
    SCORE_MULTIPLIER,
    SCREEN_SIZE,
)
from gamestate import GameState
from obstaclefield import ObstacleField
from player import Player


def display_score(screen, start_time):
    font = pygame.font.SysFont("sans-serif", 25)
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(topleft=(10, 10))
    screen.blit(score_surface, score_rect)


def title_screen(screen):
    start_btn = Button(
        center_position=(400, 200),
        font_size=30,
        bg_rgb=BACKGROUND_COLOUR,
        text_rgb=GROUND_COLOUR,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = Button(
        center_position=(400, 250),
        font_size=30,
        bg_rgb=BACKGROUND_COLOUR,
        text_rgb=GROUND_COLOUR,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = [start_btn, quit_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BACKGROUND_COLOUR)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()



def main() -> None:
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Dino Game")

    clock = pygame.time.Clock()
    fps = 60
    dt = 0
    start_time = int(pygame.time.get_ticks() / 1000)

    background = pygame.Surface(SCREEN_SIZE)
    background.fill(BACKGROUND_COLOUR)

    ground = pygame.Surface(GROUND_SIZE)
    ground_rect = ground.get_rect(bottomleft=(0, 400))
    ground.fill(GROUND_COLOUR)

    player = pygame.sprite.GroupSingle()
    text_font = pygame.font.SysFont(FONT, 25)
    player.add(Player(text_font, " player-test "))

    obstacles = pygame.sprite.Group()
    field = ObstacleField(obstacles)

    score = 0
    game_state = GameState.TITLE

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(score)
                pygame.quit()
                exit()

        if game_state == GameState.TITLE:
            game_state = title_screen(screen)
            #resetting the score back to 0 once the starts over again
            if game_state == GameState.NEWGAME:
                score = 0
                start_time = int(pygame.time.get_ticks()/1000)
                #starts the obstacles from the beginning/fresh
                obstacles.empty()

        if game_state == GameState.QUIT:
            pygame.quit()
            return

        if game_state == GameState.NEWGAME:
            for o in obstacles:
                if o.rect.colliderect(player.sprite.rect):
                    print(score)
                    game_state = GameState.TITLE

            obstacles.update(dt)
            field.update(dt)
            player.update()

            score += dt * SCORE_MULTIPLIER

        screen.blit(background, (0, 0))
        screen.blit(ground, ground_rect)
        player.draw(screen)
        pygame.draw.rect(screen, PLAYER_USERNAME_BACKGROUND, player.sprite.name_rect)
        screen.blit(player.sprite.name, player.sprite.name_rect)
        obstacles.draw(screen)
        display_score(screen, start_time)

        pygame.display.flip()
        time = clock.tick(fps)
        dt = time / 1000



if __name__ == "__main__":
    main()
