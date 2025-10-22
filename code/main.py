import pygame
from os.path import join
from random import randint

# General set up
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
pygame.display.set_caption("My first game")
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Plain Surface
surface = pygame.Surface((100, 200))
surface.fill('gray')

# importing form image
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()

star_pos = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)]


running = True
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the game

    display_surface.fill('darkgray')
    display_surface.blit(player_surf, (10, 20))
    for pos in star_pos:
        display_surface.blit(star_surf, pos)
    pygame.display.update()


pygame.quit()