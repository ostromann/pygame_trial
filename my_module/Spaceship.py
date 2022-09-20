import pygame
import pymunk

from my_module.Bullet import Bullet
from my_module.Spritesheet import Spritesheet
from . import config
from . import assets
from . import utils
import math
import numpy as np


# TODO: Disable collision between Bullets and Spaceship
class Spaceship(pymunk.Poly):
    def __init__(self, pos):
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.position = pos

        self.size = config.spaceship_size

        w, h = self.size[0], self.size[1]
        vs = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]

        super().__init__(body, vs)
        self.mass = config.spaceship_mass
        self.elasticity = 0.4
        self.friction = 0.4
        self.color = (255, 255, 0, 100)
        self.collision_type = config.collision_types['spaceship']

        self.filter = pymunk.ShapeFilter(
            categories=config.object_categories['player'], mask=config.category_masks['player'])
        self.image = pygame.transform.scale(
            assets.images['spaceship'], self.size)

        self.acc_direction = np.array([0.0, 0.0])
        self.vel = np.array([0.0, 0.0])
        self.max_vel = 800  # px/frame
        self.acc = 50  # px/frame^2
        self.friction = 0.9  # px/frame^2
        self.max_health = 3
        self.health = self.max_health
        self.max_bullets = 10
        self.bullets = []
        self.bullet_vel = 10
        self.invincible = 0
        self.skin = 3

        self.weapons = [(0, 0), (8, 0)]

        self.image_shield = pygame.transform.scale(
            assets.images['shield'], (self.size[0]/(self.max_health+1), self.size[0]/(self.max_health+1)))

        sprite_sheet = Spritesheet(assets.sprites['spaceships'])
        self.sprites = []
        for i in range(0, 3):
            self.sprites.append(pygame.transform.scale(sprite_sheet.get_sprite(
                i, self.skin, 8, 8), (self.size[0], self.size[0])))

        sprite_sheet = Spritesheet(assets.sprites['miscellaneous'])
        self.engine_sprites = []
        for i in range(0, 4):
            self.engine_sprites.append(pygame.transform.scale(sprite_sheet.get_sprite(
                5+i, 3, 8, 8), (self.size[0], self.size[0])))

        self.sprite_pointer = 0

    def handle_acceleration(self, keys_pressed):
        self.acc_direction = np.array([0.0, 0.0])

        if keys_pressed[config.keys['left']]:
            self.acc_direction[0] -= 1.0
        if keys_pressed[config.keys['right']]:
            self.acc_direction[0] += 1.0
        if keys_pressed[config.keys['up']]:
            self.acc_direction[1] -= 1.0
        if keys_pressed[config.keys['down']]:
            self.acc_direction[1] += 1.0

        # if no key pressed, apply friction
        if self.acc_direction[0] == 0.0 and self.acc_direction[1] == 0.0:
            self.vel = np.array([0.0, 0.0]) if np.linalg.norm(
                self.vel) < 0.01 else self.vel * self.friction

        # apply acceleration
        else:
            # normalize acceleration to unit vector
            self.acc_direction = self.acc_direction / \
                np.linalg.norm(self.acc_direction)
            self.acc_direction = np.where(
                np.isnan(self.acc_direction), 0, self.acc_direction)

            self.vel += self.acc_direction * self.acc

        # limit velocity
        if np.linalg.norm(self.vel) > self.max_vel:
            v_hat = self.vel / np.linalg.norm(self.vel)
            self.vel = v_hat * self.max_vel

    def handle_movement(self, keys_pressed, win):
        pass
        self.handle_acceleration(keys_pressed)

        self.body.velocity = (self.vel[0], self.vel[1])

        x, y = self._get_body().position
        w, h = self.size
        w /= 2
        h /= 2
        win_height = win.get_height()
        win_width = win.get_width()

        # check boundary collision
        boundary_collision = False
        if x - w < 0:
            x = 0 + w
            self.vel[0] = 0.0
            boundary_collision = True
        if x + w > win_width:
            x = win_width - w
            self.vel[0] = 0.0
            boundary_collision = True
        if y - h < 0:
            y = 0 + h
            self.vel[1] = 0.0
            boundary_collision = True
        if y + h > win_height:
            y = win_height - h
            self.vel[1] = 0.0
            boundary_collision = True

        if boundary_collision:
            self.body.position = (x, y)

    def shoot(self):
        angle = math.degrees(-self._get_body().angle)
        x, y = self._get_body().position
        w, h = self.size[0], self.size[1]
        x -= w / 2
        y -= h / 2

        bullets = []
        self.weapons = [(-3*config.scale, -5*config.scale - 5*config.scale),
                        (+3*config.scale, -5*config.scale - 5*config.scale)]
        for weapon in self.weapons:
            x, y = self._get_body().position + weapon
            print('Spaceship:', self._get_body().position, 'Bullet:', x, y)
            bullets.append(
                Bullet((x, y), (1*config.scale, 10*config.scale), 5))
        return bullets

    def draw(self, win, bullets):

        # Render spaceship
        angle = math.degrees(-self._get_body().angle)
        x, y = self._get_body().position
        w, h = self.size[0], self.size[1]
        x -= w / 2
        y -= h / 2

        # Render spaceship
        if self.acc_direction[0] > 0.0:
            utils.blitRotate2(win, self.sprites[2], (x, y), angle)
        elif self.acc_direction[0] < 0.0:
            utils.blitRotate2(win, self.sprites[0], (x, y), angle)
        else:
            utils.blitRotate2(win, self.sprites[1], (x, y), angle)

        # Render Engine flame
        utils.blitRotate2(
            win, self.engine_sprites[self.sprite_pointer//4], (x, y+h), angle)
        self.sprite_pointer += 1
        self.sprite_pointer %= 4*4

        # # Render available bullets
        # for pos, slot in enumerate(range(self.max_bullets - len(bullets))):
        #     slot_width = w//self.max_bullets-2
        #     slot_height = 10
        #     pygame.draw.rect(win, self.color, pygame.Rect(
        #         x + (slot_width + 2)*pos, y-slot_height, slot_width, slot_height))

        # # Render shields
        # for pos, slot in enumerate(range(self.health)):
        #     win.blit(self.image_shield, (x + 10*pos, y + h))
