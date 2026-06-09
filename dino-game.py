from sys import exit
import pygame
from constants import (BACKGROUND_COLOUR, GROUND_COLOUR, GROUND_SIZE,
                       PLAYER_USERNAME_FONT, SCORE_MULTIPLIER, SCREEN_SIZE)
from obstaclefield import ObstacleField
from player import Player


def main() -> None:
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Dino Game")
    
    clock = pygame.time.Clock()
    fps = 60
    dt = 0

    background = pygame.Surface(SCREEN_SIZE)
    background.fill(BACKGROUND_COLOUR)

    ground = pygame.Surface(GROUND_SIZE)
    ground_rect = ground.get_rect(bottomleft=(0, 400))
    ground.fill(GROUND_COLOUR)

    player = pygame.sprite.GroupSingle()
    text_font = pygame.font.SysFont(PLAYER_USERNAME_FONT, 25)
    player.add(Player(text_font, "player-test"))

    obstacles = pygame.sprite.Group()
    field = ObstacleField(obstacles)

    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(score)
                pygame.quit()
                exit()

        if not game_over:
            for o in obstacles:
                if o.rect.colliderect(player.sprite.rect):
                    print(score)
                    game_over = True
            
            obstacles.update(dt)
            field.update(dt)
            player.update()

        screen.blit(background, (0, 0))
        screen.blit(ground, ground_rect)
        player.draw(screen)
        screen.blit(player.sprite.name, player.sprite.name_rect)
        obstacles.draw(screen)

        pygame.display.flip()
        time = clock.tick(fps)
        dt = time/1000
        
        if not game_over:
            score += dt * SCORE_MULTIPLIER

if __name__ == "__main__":
    main()
