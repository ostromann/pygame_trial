import pymunk
import pygame
import math
from . import utils
from . import config


class Asteroid(pymunk.Circle):
    def __init__(self, pos, radius, mass, image):
        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = pos

        super().__init__(body, radius, offset=(0, 0))
        self.mass = mass
        self.elasticity = 0.4
        self.friction = 0.4
        self.color = (255, 0, 0, 0)
        self.collision_type = config.collision_types['asteroid']
        self.image = pygame.transform.scale(
            image, (self.radius*2, self.radius*2))

    def draw(self, win):
        angle = math.degrees(-self._get_body().angle)
        x, y = self._get_body().position

        utils.blitRotate2(win, self.image, (int(
            x-self.radius), int(y-self.radius)), angle)

    def is_out_of_bounds(self):
        x, y = self._get_body().position
        if x < 200:
            return True
        if y < -50 or y > 500:
            return True
        return False
