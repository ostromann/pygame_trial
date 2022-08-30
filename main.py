import ast
from cmath import isnan
import sys
import os
import pygame
import pymunk
import pymunk.pygame_util
import numpy as np
import math

from my_module.Explosion import Explosion
from my_module.Spaceship import Spaceship
from my_module.Bullet import Bullet
from my_module.Wave import Wave
from my_module import config


pygame.font.init()

WIN = pygame.display.set_mode((config.screen_width, config.screen_height))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 55

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)


# load background image
SPACE = pygame.image.load(os.path.join(
    'Assets', 'space_endless.png')).convert()

STARS = pygame.image.load(os.path.join(
    'Assets', 'stars.png')).convert_alpha()

SHIELD_WIDTH, SHIELD_HEIGHT = 10, 10

YELLOW_SHIELD = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'shield_yellow.png')), (SHIELD_WIDTH, SHIELD_HEIGHT))
RED_SHIELD = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'shield_red.png')), (SHIELD_WIDTH, SHIELD_HEIGHT))

ASTEROID = pygame.image.load(os.path.join('Assets', 'asteroid.png'))
BULLET = pygame.image.load(os.path.join('Assets', 'bullet.png'))

DEBUG_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'debug.png')), (40, 40))


def remove_asteroid_and_bullet(arbiter, space, data):
    a = arbiter.shapes[0]  # Asteroid
    b = arbiter.shapes[1]  # Bullet

    print(a)
    # Spawn explosion
    print(
        f'create explosion at: {a._get_body().position} with size {a.radius} x {a.radius}')
    data['explosions'].append(Explosion(a._get_body().position, a.radius))

    # Remove asteroid
    space.remove(a, a.body)
    try:
        data['asteroids'].remove(a)
    except ValueError:
        pass
    # Remove bullet
    space.remove(b, b.body)
    try:
        data['bullets'].remove(b)
    except ValueError:
        pass


class Ammo(pygame.Rect):
    def __init__(self, x=config.screen_width, y=0, width=30, height=30):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), self)


class Background():
    def __init__(self, image,  scroll_speed):
        self.image = image
        self.tiles = math.ceil(config.screen_width /
                               self.image.get_width()) + 1
        self.scroll_speed = scroll_speed
        self.scroll = 0

    def draw(self, win):
        # draw scrolling background
        for i in range(0, self.tiles):
            WIN.blit(self.image, (i * self.image.get_width() + self.scroll, 0))

        # scroll background
        self.scroll += self.scroll_speed

        # reset scroll
        if abs(self.scroll) > self.image.get_width():
            self.scroll = 0


def draw_window(space, draw_options, backgrounds, spaceships,  bullets, explosions, asteroids, items, pushers):
    for background in backgrounds:
        background.draw(WIN)

    for spaceship in spaceships:
        spaceship.draw(WIN, bullets)

    for bullet in bullets:
        if bullet.is_out_of_bounds():
            space.remove(bullet.body, bullet)
            bullets.remove(bullet)
        else:
            bullet.draw(WIN)

    for explosion in explosions:
        if not explosion.draw(WIN):
            explosions.remove(explosion)

    for asteroid in asteroids:
        if asteroid.is_out_of_bounds():
            space.remove(asteroid.body, asteroid)
            asteroids.remove(asteroid)
        else:
            asteroid.draw(WIN)

    for pusher in pushers:
        if pusher.is_out_of_bounds():
            space.remove(pusher.body, pusher.shape)
            pushers.remove(pusher)

    for item in items:
        item.draw(WIN)


def main():
    space_background = Background(SPACE, -1)
    stars_background = Background(STARS, -2)
    yellow = Spaceship(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT, YELLOW_SPACESHIP_IMAGE,
                       pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE, YELLOW_HIT)

    backgrounds = [space_background, stars_background]
    spaceships = [yellow]
    bullets = []
    explosions = []
    asteroids = []
    items = []
    waves = []
    pushers = []

    # Pymunk stuff
    draw_options = pymunk.pygame_util.DrawOptions(WIN)
    space = pymunk.Space()
    space.gravity = (0, 0)  # y increases downward in pygame

    h = space.add_collision_handler(
        config.collision_types["asteroid"], config.collision_types["bullet"])

    h.data['asteroids'] = asteroids
    h.data['bullets'] = bullets
    h.data['explosions'] = explosions

    h.post_solve = remove_asteroid_and_bullet

    # Game setting
    wave_countdown = 10
    wave_interval = 200

    clock = pygame.time.Clock()
    run = True
    while run:
        space.step(config.dt)
        clock.tick(config.fps)

        wave_countdown -= 1

        if wave_countdown == 0:
            wave_countdown = wave_interval
            wave = Wave(2, 10, [20, 30, 40], 2000000)
            waves.append(wave)
            for asteroid in wave.asteroids:
                asteroids.append(asteroid)
            pushers.append(wave.pusher)
            wave.launch(space)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                for spaceship in spaceships:
                    if event.key == spaceship.key_shoot and len(bullets) < spaceship.max_bullets:
                        bullet = Bullet((spaceship.x+spaceship.width, spaceship.y +
                                         spaceship.height//2 - 2), (20, 5), 5)
                        # bullet = Bullet((30, 250), (20, 30), 10, BULLET)
                        space.add(bullet.body, bullet)
                        bullets.append(bullet)
                        spaceship.bullets.append(bullet)
                        # Shoot
                        bullet.body.apply_impulse_at_local_point(
                            (2000, 0), (0, 0))

            if event.type == YELLOW_HIT:
                explosion = Explosion(yellow.x + yellow.width/2, yellow.y + yellow.height/2,
                                      yellow.width, yellow.height, config.explosion_timeout)
                explosions.append(explosion)
                yellow.health -= 1

        keys_pressed = pygame.key.get_pressed()
        yellow.handle_movement(keys_pressed, WIN)

        draw_window(space, draw_options,  backgrounds, spaceships, bullets,
                    explosions, asteroids, items, pushers)

        # space.debug_draw(draw_options)
        # pygame.display.update()
        pygame.display.flip()

    main()


if __name__ == "__main__":
    main()
