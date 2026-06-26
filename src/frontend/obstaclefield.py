import random
import pygame
from .constants import OBSTACLE_SPAWN_POINT, SPAWN_RATE, MIN_SPAWN_RATE, SPAWNRATE_SCALE
from .obstacle import Obstacle


class ObstacleField(pygame.sprite.Sprite):

    def __init__(self, group: pygame.sprite.Group) -> None:
        super().__init__()
        self.spawn_timer = 0.0
        self.spawn_point = OBSTACLE_SPAWN_POINT
        self.group = group

    def spawn(self, scale, spawn_point):
        obstacle = Obstacle(scale, spawn_point)
        self.group.add(obstacle)

    def update(self, dt: float, score: float):
        self.spawn_timer += dt
        spawn_rate = max(MIN_SPAWN_RATE, SPAWN_RATE - score * SPAWNRATE_SCALE) # increasing spawn rate with increasing score (i.e. time)
        if self.spawn_timer > spawn_rate:
            self.spawn_timer = 0

            scale = random.choice([0.5, 1, 1.5])
            self.spawn(scale, self.spawn_point)
