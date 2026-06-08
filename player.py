import pygame
from constants import PLAYER_COLOUR, PLAYER_SIZE

class Player(pygame.sprite.Sprite):
    def __init__(self, username):
        super().__init__()
        # player, rectangle size
        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(PLAYER_COLOUR)
        # placement of player, rectangle
        self.rect = self.image.get_rect(center=(80, 250))
        self.gravity = 0

    # user input up-arrow for movement
    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.rect.bottom >= 250:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 250:
            self.rect.bottom = 250

    def update(self):
        self.player_input()
        self.apply_gravity()
