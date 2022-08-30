import math
import pygame
import pymunk
import numpy as np
from .Asteroid import Asteroid
from .Pusher import Pusher
from . import config


''' TODO: Is it a good idea to create waves like this with a string
----L-M-S----MMM-L---
--L--S-S-S--L---L----
where:
-: no asteroid
L: large asteroid
M: medium
S: small

could also spawn items in the same way etc.
'''


class Wave():
    def __init__(self, rows, cols, asteroid_radii, force):
        # TODO: Do something something smart here for the placement
        self.pos = (1200, 200)
        self.rows = rows
        self.cols = cols
        self.asteroid_radii = asteroid_radii
        self.force = force
        self.asteroids = []
        self.spawn_asteroids()
        # TODO: perhaps this can be done nicer
        self.pusher = Pusher((self.pos[0]+300, self.pos[1]), (20, 1200), 10000)

    def spawn_asteroids(self):
        for i in range(0, self.cols):
            for j in range(0, self.rows):
                x, y = self.pos
                grid_size = np.max(self.asteroid_radii)
                spawn_point = (x + j * grid_size, y + i * grid_size)
                radius = np.random.choice(self.asteroid_radii)
                mass = 4/3 * math.pi * radius**3 * config.asteroid_density
                self.asteroids.append(
                    Asteroid(spawn_point, radius, mass))

    def launch(self, space):
        # Add asteroids
        for asteroid in self.asteroids:
            space.add(asteroid.body, asteroid)

        # Add Pusher
        space.add(self.pusher.body, self.pusher.shape)

        # Launch
        self.pusher.body.apply_impulse_at_local_point(
            (-self.force, 0), (0, 0))
