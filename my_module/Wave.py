import pygame
import pymunk
import numpy as np
from .Asteroid import Asteroid
from .Pusher import Pusher


class Wave():
    def __init__(self, rows, cols, asteroid_sizes, force, image):
        # TODO: Do something something smart here for the placement
        self.pos = (1200, 200)
        self.rows = rows
        self.cols = cols
        self.asteroid_sizes = asteroid_sizes
        self.force = force
        self.image = image
        self.asteroids = []
        self.spawn_asteroids()
        # TODO: perhaps this can be done nicer
        self.pusher = Pusher((self.pos[0]+300, self.pos[1]), (20, 1200), 10000)

    def spawn_asteroids(self):
        for i in range(0, self.cols):
            for j in range(0, self.rows):
                x, y = self.pos
                grid_size = np.max(self.asteroid_sizes)
                spawn_point = (x + j * grid_size, y + i * grid_size)
                size = np.random.choice(self.asteroid_sizes)
                mass = size * 5  # TODO: Compute mass based on volume

                # TODO: The asteroid image (as all other, should perhaps be globally accessible?)
                self.asteroids.append(
                    Asteroid(spawn_point, size, mass, self.image))

    # def spawn_pusher(self):
    #     body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    #     body.position = (self.pos[0]+300, self.pos[1])
    #     shape = pymunk.Poly.create_box(body, (20, 1200))
    #     shape.mass = 10000
    #     shape.elasticity = 0.5
    #     shape.friction = 0.5

    #     return body, shape

    def launch(self, space):
        # Add asteroids
        for asteroid in self.asteroids:
            space.add(asteroid.body, asteroid.shape)

        # Add Pusher
        space.add(self.pusher.body, self.pusher.shape)

        # Launch
        self.pusher.body.apply_impulse_at_local_point(
            (-self.force, 0), (0, 0))
