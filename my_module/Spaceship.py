import pygame
from . import config
from . import assets
import numpy as np


# TODO: Make to pymunk.Poly
class Spaceship(pygame.Rect):
    def __init__(self, x, y, width, height):
        # self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(
            assets.images['spaceship'], (width, height))
        self.color = (255, 255, 0)
        self.vel = np.array([0.0, 0.0])
        self.max_vel = 20  # px/frame
        self.acc = 0.8  # px/frame^2
        self.friction = 0.9  # px/frame^2
        self.max_health = 5
        self.health = self.max_health
        self.max_bullets = 10
        self.bullets = []
        self.bullet_vel = 10

    def handle_acceleration(self, keys_pressed):
        acc_direction = np.array([0.0, 0.0])

        if keys_pressed[config.keys['left']]:
            acc_direction[0] -= 1.0
        if keys_pressed[config.keys['right']]:
            acc_direction[0] += 1.0
        if keys_pressed[config.keys['up']]:
            acc_direction[1] -= 1.0
        if keys_pressed[config.keys['down']]:
            acc_direction[1] += 1.0

        # if no key pressed, apply friction
        if acc_direction[0] == 0.0 and acc_direction[1] == 0.0:
            self.vel = np.array([0.0, 0.0]) if np.linalg.norm(
                self.vel) < 0.01 else self.vel * self.friction

        # apply acceleration
        else:
            # normalize acceleration to unit vector
            acc_direction = acc_direction / np.linalg.norm(acc_direction)
            acc_direction = np.where(np.isnan(acc_direction), 0, acc_direction)

            self.vel += acc_direction * self.acc

        # limit velocity
        if np.linalg.norm(self.vel) > self.max_vel:
            # print('reached max vel')
            v_hat = self.vel / np.linalg.norm(self.vel)
            # print('unit vector', v_hat)
            self.vel = v_hat * self.max_vel
            # print('limited', self.vel)

    def handle_movement(self, keys_pressed, win):
        self.handle_acceleration(keys_pressed)

        self.x += self.vel[0]
        self.y += self.vel[1]

        win_height = win.get_height()
        win_width = win.get_width()

        # check boundary collision
        if self.x < 0:
            self.x = 0
            self.vel[0] = 0.0
        if self.x + self.width > win_width:
            self.x = win_width - self.width
            self.vel[0] = 0.0
        if self.y < 0:
            self.y = 0
            self.vel[1] = 0.0
        if self.y + self.height > win_height:
            self.y = win_height - self.height
            self.vel[1] = 0.0

    # def handle_collisions(self, asteroids, items):
        # for asteroid in asteroids:
        #     print('checking collisions with', asteroid)
        #     if self.colliderect(asteroid):
        #         items.append(Ammo(self.x, self.y))
        #         asteroids.remove(asteroid)
        #         pygame.event.post(pygame.event.Event(YELLOW_HIT))

    def draw(self, win, bullets):
        # Render spaceship
        win.blit(self.image, (self.x, self.y))

        # Render available bullets
        for pos, slot in enumerate(range(self.max_bullets - len(bullets))):
            slot_width = self.width//self.max_bullets-2
            slot_height = 10
            pygame.draw.rect(win, self.color, pygame.Rect(
                self.x + (slot_width + 2)*pos, self.y-slot_height, slot_width, slot_height))

        # # Render shields
        # for pos, slot in enumerate(range(self.health)):
        #     if self.color == YELLOW:
        #         win.blit(YELLOW_SHIELD, (self.x + 10*pos,
        #                                  self.y + self.height))
        #     elif self.color == RED:
        #         win.blit(RED_SHIELD, (self.x + 10*pos,
        #                               self.y + self.height))
