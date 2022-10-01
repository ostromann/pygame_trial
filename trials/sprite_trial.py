import pygame
from Spritesheet import Spritesheet

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

# sprite_sheet_image = pygame.image.load(
#     'Assets/spaceship_sprites.png').convert_alpha()
sprite_sheet = Spritesheet('Assets/spaceship_sprites.png')

BG = (50, 50, 50)
BLACK = (0, 0, 0)


frame_0 = sprite_sheet.get_sprite(0, 0, 32, 32)
frame_1 = sprite_sheet.get_sprite(1, 0, 32, 32)
frame_2 = sprite_sheet.get_sprite(2, 0, 32, 32)
frame_3 = sprite_sheet.get_sprite(3, 0, 32, 32)

run = True
while run:

    # update background
    screen.fill(BG)

    # show frame image
    screen.blit(frame_0, (0, 0))
    screen.blit(frame_1, (72, 0))
    screen.blit(frame_2, (150, 0))
    screen.blit(frame_3, (250, 0))

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
