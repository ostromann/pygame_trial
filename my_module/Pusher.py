import pygame
import pymunk
from . import utils
import math


class Pusher(pymunk.Poly):
    def __init__(self, pos, size, mass):
        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = pos

        self.size = size

        w, h = size[0], size[1]
        vs = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]

        super().__init__(body, vs)
        self.mass = mass
        self.elasticity = 0.5
        self.friction = 0.5

    def is_out_of_bounds(self):
        x, y = self._get_body().position
        if y > 100:
            return True
        return False
