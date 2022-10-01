import pymunk
import pygame
import math

from my_module.Spritesheet import Spritesheet
from . import config
from . import assets
from . import utils
import os


class ShieldMask():
    def __init__(self, pos, impact):
        self.pos = pos
        self.radius = 0
        self.max_radius = impact / 100
        self.growth_speed = 10

        self.duration = 0
        self.max_duration = impact / 60
        self.image = pygame.image.load(
            os.path.join('Assets', 'mask.png'))
        # assets.sounds['explosion'].play()

    def draw(self, win):
        if self.duration < self.max_duration:
            # increase radius to mimic effect on the shield after impact

            self.radius += self.growth_speed
            x, y = self.pos

            # Calculate new alpha
            alpha = (1 - (self.duration/self.max_duration)**2)*100
            print(f'alpha: {alpha}, {self.duration}/{self.max_duration}')

            # Adjsut alpha and set new size
            self.image.set_alpha(alpha)
            tmp_image = pygame.transform.scale(
                self.image, (self.radius*2, self.radius*2))

            tmp_surf = pygame.Surface(
                (config.display_w, config.display_h), pygame.SRCALPHA)

            tmp_surf.blit(tmp_image, (int(
                x-self.radius), int(y-self.radius)))
            tmp_surf.blit(tmp_image, (int(
                x-self.radius), int(y-self.radius)), special_flags=pygame.BLEND_RGB_SUB)
            win.blit(tmp_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

            # win.blit(tmp_image, (int(
            #     x-self.radius), int(y-self.radius)), special_flags=pygame.BLEND_RGBA_ADD)

            # self.mask = pygame.mask.from_surface()

            self.duration += 1
            return True
        return False
