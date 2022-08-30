import pymunk
import pygame
import math
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

    def draw(self, win):
        if self.duration > 0:
            angle = math.degrees(-self._get_body().angle)
            x, y = self._get_body().position

            utils.blitRotate2(win, self.image, (int(
                x-self.radius), int(y-self.radius)), angle)
            self.duration -= 1
            return True
        return False
