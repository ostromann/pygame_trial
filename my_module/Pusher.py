import pygame
import pymunk
from . import utils
import math


class Pusher():
    def __init__(self, pos, size, mass):
        self.pos = pos
        self.size = size
        self.mass = mass
        self.body, self.shape = self.create_body_and_shape()

    def create_body_and_shape(self):
        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = self.pos
        shape = pymunk.Poly.create_box(body, (20, 1200))
        shape.mass = 10000
        shape.elasticity = 0.5
        shape.friction = 0.5

        return body, shape

    def get_body_shape(self):
        return self.body, self.shape

    def is_out_of_bounds(self):
        x, y = self.shape._get_body().position
        if x < 1200:
            return True
        return False
