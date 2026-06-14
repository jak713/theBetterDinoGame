import pygame
from game.constants import OBSTACLE_COLOUR, OBSTACLE_SIZE, OBSTACLE_SPEED_MULT


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, scale, spawn_point):
        super().__init__()
        size = (OBSTACLE_SIZE[0] * scale, OBSTACLE_SIZE[1])
        self.image = pygame.Surface(size)
        self.image.fill(OBSTACLE_COLOUR)
        self.rect = self.image.get_rect(bottomleft=spawn_point)

    def update(self, dt):
        self.rect.x -= dt * OBSTACLE_SPEED_MULT
        if self.rect.right < 0:
            self.kill()
