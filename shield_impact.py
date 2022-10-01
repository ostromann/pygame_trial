from email.mime import base
import sys
import os
import pygame
import pymunk
import pymunk.pygame_util

import numpy as np


from my_module.Bullet import Bullet
from my_module.Explosion import Explosion
from my_module.Shield import Shield
from my_module.ShieldMask import ShieldMask
from my_module.Background import Background
from my_module.Spaceship import Spaceship
from my_module.Spritesheet import Spritesheet
from my_module import config
from my_module import assets

pygame.font.init()
WIN = pygame.display.set_mode((config.display_w, config.display_h))
pygame.display.set_caption("Asteroid Impact")


def shield_collision(arbiter, space, data):
    # if arbiter.is_first_contact:
    print('collision!')
    contact_point = (
        arbiter.contact_point_set.points[0].point_a[0], arbiter.contact_point_set.points[0].point_a[1])
    print('contact_point', contact_point)
    print('impulse', arbiter.total_impulse.length)

    data['shield_masks'].append(ShieldMask(
        contact_point, arbiter.total_impulse.length))

    # data['shield_masks'].append(ShieldMask())

    # Spawn a circle that grows and dims out and use it as mask for drawing the Shield


def main():
    # Pymunk stuff
    draw_options = pymunk.pygame_util.DrawOptions(WIN)
    space = pymunk.Space()
    space.gravity = (0, 0)  # y increases downward in pygame

    shield_masks = []

    shadow_surf = pygame.Surface(
        (config.display_w, config.display_h), pygame.SRCALPHA)

    # Collision
    h = space.add_collision_handler(
        config.collision_types["shield"], config.collision_types["bullet"])
    h.data['shield_masks'] = shield_masks
    h.post_solve = shield_collision

    clock = pygame.time.Clock()
    run = True
    frame = 0
    while run:
        if frame == 0:
            # Spawn items
            shield = Shield((200, 200), 100, 10000)
            bullet = Bullet((100 + np.random.uniform(0, 200),
                             config.display_h), (10, 10), 5)

            space.add(shield.body, shield)
            space.add(bullet.body, bullet)
            bullet.body.apply_impulse_at_local_point(
                (0, np.random.uniform(-2000, -1000)), (0, 0))

            shield_masks.append(ShieldMask(
                (config.display_w, config.display_h), 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        space.step(config.dt)
        clock.tick(config.fps)

        WIN.fill((0, 0, 0))
        shadow_surf.fill((0, 0, 0, 0))  # Clear the shadow_surf each frame.

        bullet.draw(WIN)
        shield.draw(shadow_surf)

        for shield_mask in shield_masks:
            shield_mask.draw(shadow_surf)

        WIN.blit(shadow_surf, (0, 0))

        # WIN.blit()

        # space.debug_draw(draw_options)

        pygame.display.flip()
        frame += 1

        if frame == 100:
            space.remove(shield.body, shield)
            space.remove(bullet.body, bullet)
            frame = 0
    main()


if __name__ == "__main__":
    main()
