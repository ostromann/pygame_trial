# from email.mime import base
# import sys
import pygame
import sys
import os
# import pygame
# import pymunk
# import pymunk.pygame_util

# import numpy as np


# from my_module.Bullet import Bullet
# from my_module.Explosion import Explosion
# from my_module.Shield import Shield
# from my_module.ShieldMask import ShieldMask
# from my_module.Background import Background
# from my_module.Spaceship import Spaceship
# from my_module.Spritesheet import Spritesheet
# from my_module import config
# from my_module import assets

# pygame.font.init()
# WIN = pygame.display.set_mode((100, 100))
# pygame.display.set_caption("Asteroid Impact")


# def main():
#     shadow_surf = pygame.Surface(
#         (100, 100), pygame.SRCALPHA)

#     clock = pygame.time.Clock()
#     run = True
#     frame = 0
#     while run:
#         if frame == 0:
#             # Spawn items
#             objects = [
#                 pygame.Rect(20, 30, 1, 1),
#                 pygame.Rect(50, 70, 1, 1),
#                 pygame.Rect(80, 90, 1, 1),
#             ]

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#                 pygame.quit()
#                 sys.exit()

#         clock.tick(config.fps)

#         WIN.fill((0, 0, 0))
#         shadow_surf.fill((0, 0, 0, 0))  # Clear the shadow_surf each frame.

#         pygame.draw(pygame.line)

#         for shield_mask in shield_masks:
#             shield_mask.draw(shadow_surf)

#         WIN.blit(shadow_surf, (0, 0))

#         # WIN.blit()

#         space.debug_draw(draw_options)

#         pygame.display.flip()
#         frame += 1

#         if frame == 100:
#             space.remove(shield.body, shield)
#             space.remove(bullet.body, bullet)
#             frame = 0
#     main()


# if __name__ == "__main__":
#     main()

def blitRotate2(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)


pygame.init()

screen = pygame.display.set_mode((200, 200))
FPSCLOCK = pygame.time.Clock()
GREEN = pygame.Color("green")
COLOR = (0, 255, 155)  # GREEN
startpoint = pygame.math.Vector2(100, 100)
endpoint = pygame.math.Vector2(100, 0)
angle = 0
done = False

radar_alpha = pygame.image.load(os.path.join('Assets', 'radar_alpha.png'))

# Spawn items
objects = [
    pygame.Rect(40, 130, 5, 5),
    pygame.Rect(50, 70, 5, 5),
    pygame.Rect(120, 90, 5, 5),
]

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # % 360 to keep the angle between 0 and 360.
    angle = (angle+2) % 360
    # The current endpoint is the startpoint vector + the
    # rotated original endpoint vector.
    current_endpoint = startpoint + endpoint.rotate(angle)

    surf = pygame.Surface((200, 200))
    surf.fill((0, 0, 0))

    # Circles
    for i in range(0, 10):
        radius = 100 - i * 10
        print(radius)
        alpha = 70 - i * 10
        tmp_surf = pygame.Surface((200, 200))
        tmp_surf.set_colorkey((0, 0, 0))
        tmp_surf.set_alpha(alpha)
        pygame.draw.circle(tmp_surf, COLOR, (100, 100), radius, 10)
        surf.blit(tmp_surf, (0, 0))

    # Circles
    for i in range(0, 10):
        radius = 100 - i * 10
        print(radius)
        alpha = 100 - i * 10
        tmp_surf = pygame.Surface((200, 200))
        tmp_surf.set_colorkey((0, 0, 0))
        tmp_surf.set_alpha(alpha)
        pygame.draw.circle(tmp_surf, COLOR, (100, 100), radius, 2)
        surf.blit(tmp_surf, (0, 0))

    # Objects
    for object in objects:
        pygame.draw.rect(surf, COLOR, object)

    # Line
    pygame.draw.line(surf, COLOR, startpoint, current_endpoint, 4)
    screen.blit(surf, (0, 0))

    # Line Shadow
    alpha_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
    blitRotate2(alpha_surf, pygame.transform.scale(
        radar_alpha, (200, 200)), (0, 0), -angle-92)

    screen.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    pygame.display.flip()
    FPSCLOCK.tick(60)

pygame.quit()
sys.exit()
