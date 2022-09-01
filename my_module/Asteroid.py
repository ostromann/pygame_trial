import pymunk
import pygame
import math

from my_module.Spritesheet import Spritesheet
from . import utils
from . import config
from . import assets


class Asteroid(pymunk.Circle):
    def __init__(self, pos, radius, mass):
        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = pos

        super().__init__(body, radius, offset=(0, 0))
        self.mass = mass
        self.elasticity = 0.4
        self.friction = 0.4
        self.color = (255, 0, 0, 0)
        self.collision_type = config.collision_types['asteroid']

        sprite_sheet = Spritesheet(assets.sprites['miscellaneous'])
        self.image = pygame.transform.scale(sprite_sheet.get_sprite(
            1, 1, 16, 16), (self.radius*2, self.radius*2))

    def draw(self, win):
        angle = math.degrees(-self._get_body().angle)
        x, y = self._get_body().position

        utils.blitRotate2(win, self.image, (int(
            x-self.radius), int(y-self.radius)), angle)

    def is_out_of_bounds(self):
        x, y = self._get_body().position
        if x < -20:
            return True
        if y < -50 or y > config.screen_height + 50:
            return True
        return False
