import sys
import os
import pygame
import pymunk
import pymunk.pygame_util

import numpy as np

from my_module.Background import Background
from my_module.Bullet import Bullet
from my_module.Explosion import Explosion
from my_module.Item import Item
from my_module.Spaceship import Spaceship
from my_module.Spritesheet import Spritesheet
from my_module.Wave import Wave
from my_module import config
from my_module import assets

pygame.font.init()
WIN = pygame.display.set_mode((config.screen_width, config.screen_height))
pygame.display.set_caption("Asteroid Impact")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WINNER_FONT = pygame.font.SysFont('impact', 100)

# SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 55

YELLOW_HIT = pygame.USEREVENT + 1


def spaceship_hit(arbiter, space, data):
    a = arbiter.shapes[0]  # Asteroid
    b = arbiter.shapes[1]  # Ship

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

    pygame.event.post(pygame.event.Event(YELLOW_HIT))


def collect_heart(arbiter, space, data):
    a = arbiter.shapes[0]  # Spaceship
    b = arbiter.shapes[1]  # Heart

    # Remove Heart
    space.remove(b, b.body)
    try:
        data['items'].remove(b)
    except ValueError:
        pass

    print(data['spaceships'])
    data['spaceships'][0].health += 1


def remove_asteroid_and_bullet(arbiter, space, data):
    a = arbiter.shapes[0]  # Asteroid
    b = arbiter.shapes[1]  # Bullet

    # Spawn explosion
    data['explosions'].append(Explosion(a._get_body().position, a.radius*2))

    # Spawn item
    if np.random.uniform(0, 1) < a.drop_rate:
        item = Item(a._get_body().position, a.radius, 5)
        data['items'].append(item)
        space.add(item.body, item)

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

    for asteroid in asteroids:
        if asteroid.is_out_of_bounds():
            space.remove(asteroid.body, asteroid)
            asteroids.remove(asteroid)
        else:
            asteroid.draw(WIN)

    for pusher in pushers:
        if pusher.is_out_of_bounds():
            space.remove(pusher.body, pusher)
            pushers.remove(pusher)

    for item in items:
        item.draw(WIN)

    for explosion in explosions:
        if not explosion.draw(WIN):
            explosions.remove(explosion)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (config.screen_width//2 - draw_text.get_width() //
             2, config.screen_height//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    backgrounds = []
    spaceships = []
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

    # Collision
    h = space.add_collision_handler(
        config.collision_types["asteroid"], config.collision_types["bullet"])
    h.data['asteroids'] = asteroids
    h.data['bullets'] = bullets
    h.data['explosions'] = explosions
    h.data['items'] = items
    h.post_solve = remove_asteroid_and_bullet

    # Collision
    h2 = space.add_collision_handler(
        config.collision_types["asteroid"], config.collision_types["spaceship"])
    h2.data['asteroids'] = asteroids
    h2.data['explosions'] = explosions
    h2.post_solve = spaceship_hit

    # Collecting items
    h3 = space.add_collision_handler(
        config.collision_types["spaceship"], config.collision_types["item"])
    h3.data['spaceships'] = spaceships
    h3.data['items'] = items
    h3.post_solve = collect_heart

    background_sprites = Spritesheet(assets.sprites['backgrounds'])
    base_layer = pygame.transform.scale(background_sprites.get_sprite(
        0, 1, 128, 256), (config.screen_width, config.screen_height))
    bg_layer_1 = pygame.transform.scale(background_sprites.get_sprite(
        1, 1, 128, 256), (config.screen_width, config.screen_height))
    bg_layer_2 = pygame.transform.scale(background_sprites.get_sprite(
        2, 1, 128, 256), (config.screen_width, config.screen_height))

    backgrounds.append(Background(base_layer, 0, base_layer=True))
    backgrounds.append(Background(bg_layer_1, 2))
    backgrounds.append(Background(bg_layer_2, 1))
    yellow = Spaceship((100, 300))
    space.add(yellow.body, yellow)
    spaceships.append(yellow)
    # space.add(yellow.body, yellow)

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
            wave = Wave(16, 1, [8], 2000000)
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
                    if event.key == config.keys['shoot'] and len(bullets) < spaceship.max_bullets:
                        bullet = spaceship.shoot()
                        for bullet in spaceship.shoot():
                            space.add(bullet.body, bullet)
                            bullets.append(bullet)
                            spaceship.bullets.append(bullet)
                            bullet.body.apply_impulse_at_local_point(
                                (0, -1000), (0, 0))

            if event.type == YELLOW_HIT:
                yellow.invincible = 15
                yellow.health -= 1

        winner_text = ""
        if yellow.health <= 0:
            winner_text = "Game over!"

        if winner_text != "":
            draw_window(space, draw_options,  backgrounds, spaceships, bullets,
                        explosions, asteroids, items, pushers)
            draw_winner(winner_text)
            break

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
