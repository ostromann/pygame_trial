import pygame
import pymunk
import math
from . import utils
from . import config


class Bullet(pymunk.Poly):
    def __init__(self, pos, size, mass, image):
        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = pos

        self.size = size

        w, h = size[0], size[1]
        vs = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]

        super().__init__(body, vs)

        self.mass = mass
        self.elasticity = 0.4
        self.friction = 0.4
        self.color = (255, 0, 0, 100)
        self.collision_type = config.collision_types['bullet']
        self.image = pygame.transform.scale(
            image, size)
        self.sound = pygame.mixer.Sound(config.bullet_fire_sound)
        self.sound.play()

    def draw(self, win):
        angle = math.degrees(-self._get_body().angle)
        x_offset = self.size[0] / 2  # if angle = 0
        y_offset = self.size[1] / 2  # if angle = 0
        x, y = self._get_body().position

        utils.blitRotate2(win, self.image, (x-x_offset, y-y_offset), angle)

    def is_out_of_bounds(self):
        x, y = self._get_body().position
        if x < 0 or x > 1200:
            return True
        if y < -50 or y > 500:
            return True
        return False
