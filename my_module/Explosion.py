import pymunk
import pygame
import math

from my_module.Spritesheet import Spritesheet
from . import config
from . import assets
from . import utils


class Explosion(pymunk.Circle):
    def __init__(self, pos, radius):
        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = pos

        super().__init__(body, radius, offset=(0, 0))

        self.duration = config.explosion_timeout
        self.image = pygame.transform.scale(
            assets.images['explosion'], (self.radius*2, self.radius*2))
        assets.sounds['explosion'].play()

        sprite_sheet = Spritesheet(assets.sprites['miscellaneous'])
        self.sprites = []

        for i in range(0, 4):
            self.sprites.append(pygame.transform.scale(sprite_sheet.get_sprite(
                i+9, 6, 8, 8), (self.radius, self.radius)))
        self.sprite_pointer = 0

    def draw(self, win):
        if self.duration > 0:
            angle = math.degrees(-self._get_body().angle)
            x, y = self._get_body().position

            utils.blitRotate2(win, self.sprites[self.sprite_pointer//4], (int(
                x-self.radius), int(y-self.radius)), angle)

            self.sprite_pointer += 1
            self.sprite_pointer %= len(self.sprites)*4

            self.duration -= 1
            return True
        return False
