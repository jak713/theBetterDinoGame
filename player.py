import pygame
from constants import GRAVITY, PLAYER_COLOUR, PLAYER_SIZE, TREX


class Player(pygame.sprite.Sprite):
    def __init__(self, font, jump_fx: pygame.mixer.Sound, username: str = "Player"):
        super().__init__()
        # player, rectangle size
        # placement of player, rectangle
        self.image = pygame.image.load(TREX).convert_alpha()
        self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
        self.rect = self.image.get_rect(center=(80, 300))
        self.mask = pygame.mask.from_surface(self.image)

        self.gravity = 0
        self.font = font
        self.username = username
        self.name = self.font.render(self.username, True, PLAYER_COLOUR)
        self.name_rect = self.name.get_rect(midbottom=self.rect.midtop)
        self.jump_fx = jump_fx

    # user input up-arrow or space bar for movement
    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.rect.bottom >= 250:
            self.gravity = GRAVITY
            self.jump_fx.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.name_rect.midbottom = self.rect.midtop
        self.name_rect.y -= 3
