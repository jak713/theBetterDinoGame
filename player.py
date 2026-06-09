import pygame
from constants import GRAVITY, PLAYER_COLOUR, PLAYER_SIZE


class Player(pygame.sprite.Sprite):
    def __init__(self, font, username: str = "Player"):
        super().__init__()
        # player, rectangle size
        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(PLAYER_COLOUR)
        # placement of player, rectangle
        self.rect = self.image.get_rect(center=(80, 250))
        self.gravity = 0
        self.font = font
        self.username = username
        self.name = self.font.render(self.username, True, PLAYER_COLOUR)
        self.name_rect = self.name.get_rect(midbottom=self.rect.midtop)

    # user input up-arrow for movement
    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.rect.bottom >= 250:
            self.gravity = GRAVITY

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 250:
            self.rect.bottom = 250

    def update(self):

        self.player_input()
        self.apply_gravity()
        self.name_rect.midbottom = self.rect.midtop
        self.name_rect.y -= 3
