import pygame
import pymunk
import math
from . import utils
from . import config


class Bullet():
    def __init__(self, pos, size, mass, image):
        self.pos = pos
        # self.x, self.y = pos
        self.size = size
        # self.width, self.height = size
        self.mass = mass
        self.body, self.shape = self.create_body_and_shape()
        self.image = pygame.transform.scale(
            image, size)

    def create_body_and_shape(self):
        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = self.pos

        shape = pymunk.Poly.create_box(body, self.size)
        shape.mass = self.mass
        shape.elasticity = 0.4
        shape.friction = 0.4
        shape.color = (255, 0, 0, 100)
        shape.collision_type = config.collision_types['bullet']
        return body, shape

    def get_body_shape(self):
        return self.body, self.shape

    def draw(self, win):
        angle = math.degrees(-self.shape._get_body().angle)
        x_offset = self.size[0] / 2  # if angle = 0
        y_offset = self.size[1] / 2  # if angle = 0
        x, y = self.shape._get_body().position

        utils.blitRotate2(win, self.image, (x-x_offset, y-y_offset), angle)

    def is_out_of_bounds(self):
        x, y = self.shape._get_body().position
        if x < 0 or x > 1200:
            return True
        if y < -50 or y > 500:
            return True
        return False
