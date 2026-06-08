from sys import exit
import pygame

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Dino Game")

background = pygame.Surface((800, 400))
background.fill("#D5E7EE")

ground = pygame.Surface((800, 150))
ground_rect = ground.get_rect(bottomleft=(0, 400))
ground.fill("#8DA8B1")


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, username):
        super().__init__()
        # player, rectangle size
        self.image = pygame.Surface((50, 50))
        self.image.fill("#EB679E")
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


player = pygame.sprite.GroupSingle()
player.add(Player("player1"))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background, (0, 0))
    screen.blit(ground, ground_rect)
    player.draw(screen)
    player.update()

    pygame.display.update()
    clock.tick(60)
