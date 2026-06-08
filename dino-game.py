from sys import exit
import pygame
from player import Player
from obstaclefield import ObstacleField
from constants import BACKGROUND_COLOUR, GROUND_COLOUR, GROUND_SIZE, OBSTACLE_COLOUR, SCREEN_SIZE, SCORE_MULTIPLIER


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
    player.add(Player("player1"))

    obstacles = pygame.sprite.Group()
    field = ObstacleField(obstacles)

    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(score)
                pygame.quit()
                exit()

        for o in obstacles:
            if o.rect.colliderect(player.sprite.rect):
                print(score)
                return

        screen.blit(background, (0, 0))
        screen.blit(ground, ground_rect)
        player.draw(screen)
        player.update()
        field.update(dt)
        obstacles.update(dt)
        obstacles.draw(screen)

        pygame.display.flip()
        time = clock.tick(fps)
        dt = time/1000

        score += dt * SCORE_MULTIPLIER


if __name__ == "__main__":
    main()
