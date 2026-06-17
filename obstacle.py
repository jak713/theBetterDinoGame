import pygame
from constants import OBSTACLE_SIZE, OBSTACLE_SPEED_MULT


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, scale, spawn_point):
        super().__init__()
        size = (OBSTACLE_SIZE[0] * scale, OBSTACLE_SIZE[1])
        self.image = pygame.image.load("assets/tree.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(bottomleft=spawn_point)
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, dt):
        self.rect.x -= dt * OBSTACLE_SPEED_MULT
        if self.rect.right < 0:
            self.kill()
