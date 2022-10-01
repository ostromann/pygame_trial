import pymunk
import pygame
import math

from my_module.Spritesheet import Spritesheet
from . import utils
from . import config
from . import assets


class Shield(pymunk.Circle):
    def __init__(self, pos, radius, mass):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos

        super().__init__(body, radius-2, offset=(0, 0))
        self.mass = 0
        self.elasticity = 0.4
        self.friction = 0.4
        self.color = (255, 0, 0, 50)
        self.collision_type = config.collision_types['shield']
        # self.filter = pymunk.ShapeFilter(
        #     categories=config.object_categories['asteroid'], mask=config.category_masks['asteroid'])

        sprite_sheet = Spritesheet(assets.sprites['shield'])
        self.sprites = []

        for i in range(0, 4):
            sprite = pygame.transform.scale(sprite_sheet.get_sprite(
                i, 0, 32, 32), (self.radius*2, self.radius*2))
            sprite.set_alpha(0)
            self.sprites.append(sprite)
        self.sprite_pointer = 0

        print(self.sprites)

        # self.image = pygame.transform.scale(
        #     assets.images['ext_shield'], (self.radius*2, self.radius*2))
        # self.image.set_alpha(0)

        self.drop_rate = 0.5

    def draw(self, win):
        angle = math.degrees(-self._get_body().angle)
        x, y = self._get_body().position

        utils.blitRotate2(win, self.sprites[self.sprite_pointer//8], (int(
            x-self.radius), int(y-self.radius)), angle)

        self.sprite_pointer += 1
        self.sprite_pointer %= len(self.sprites)*8

    def is_out_of_bounds(self):
        x, y = self._get_body().position
        if x < -20:
            return True
        if y < -50 or y > config.display_h + 50:
            return True
        return False
