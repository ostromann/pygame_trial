import pymunk
import pygame
import math
from . import utils
from . import config


class Asteroid():
    def __init__(self, pos, radius, mass, image):
        self.pos = pos
        self.radius = radius
        self.mass = mass
        self.body, self.shape = self.create_body_and_shape()
        self.image = pygame.transform.scale(
            image, (self.radius*2, self.radius*2))

    def create_body_and_shape(self):
        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = self.pos

        shape = pymunk.Circle(body, self.radius)
        shape.mass = self.mass
        shape.elasticity = 0.4
        shape.friction = 0.4
        shape.color = (255, 0, 0, 0)
        shape.collision_type = config.collision_types['asteroid']
        return body, shape

    def get_body_shape(self):
        return self.body, self.shape

    def draw(self, win):
        angle = math.degrees(-self.shape._get_body().angle)
        x_offset = self.radius  # if angle = 0
        y_offset = self.radius  # if angle = 0
        x, y = self.shape._get_body().position

        utils.blitRotate2(win, self.image, (int(
            x-x_offset), int(y-y_offset)), angle)

    def is_out_of_bounds(self):
        x, y = self.shape._get_body().position
        if x < 200:
            return True
        if y < -50 or y > 500:
            return True
        return False
