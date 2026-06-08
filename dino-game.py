from sys import exit
import pygame
from player import Player

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
