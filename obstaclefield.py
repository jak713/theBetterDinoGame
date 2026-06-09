import random
import pygame
from constants import OBSTACLE_SPAWN_POINT, SPAWN_RATE
from obstacle import Obstacle


class ObstacleField(pygame.sprite.Sprite):
    
    def __init__(self, group) -> None:
        super().__init__()
        self.spawn_timer = 0.0
        self.spawn_point = OBSTACLE_SPAWN_POINT
        self.group = group

    def spawn(self, scale, spawn_point):
        obstacle = Obstacle(scale, spawn_point)
        self.group.add(obstacle)

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > SPAWN_RATE:
            self.spawn_timer = 0

            scale = random.choice([0.5,1,1.5])
            self.spawn(scale, self.spawn_point)

