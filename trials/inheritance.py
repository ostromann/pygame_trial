import pygame
import pymunk
import pymunk.pygame_util
import utils
import math
import os

collision_types = {
    "bullet": 1,
    "asteroid": 2,
    "ship": 3,
    "item": 4,
}


ASTEROID = pygame.image.load(os.path.join('Assets', 'asteroid.png'))
BULLET = pygame.image.load(os.path.join('Assets', 'bullet.png'))


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
        shape.collision_type = collision_types['bullet']
        return body, shape

    def get_body_shape(self):
        return self.body, self.shape

    def draw(self, win):
        angle = math.degrees(-self.shape._get_body().angle)
        x_offset = self.size[0] / 2  # if angle = 0
        y_offset = self.size[1] / 2  # if angle = 0
        x, y = self.shape._get_body().position

        utils.blitRotate2(win, self.image, (x-x_offset, y-y_offset), angle)


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
        shape.collision_type = collision_types['asteroid']
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


class Ball(pymunk.Circle):
    def __init__(self, pos, radius, image, offset=(0, 0),):
        self.image = pygame.transform.scale(
            image, (radius*2, radius*2))

        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = pos
        super().__init__(body, radius, offset)

    def draw(self, win):
        angle = math.degrees(-self._get_body().angle)
        x, y = self._get_body().position

        utils.blitRotate2(win, self.image, (int(
            x-self.radius), int(y-self.radius)), angle)


def asteroid_x_bullet(arbiter, space, data):
    print('collision!')
    print(f'arbiter: {arbiter}\nspace: {space}\ndata: {data}')
    print(f'shapes {arbiter.shapes}\nvector {arbiter.normal}')
    asteroids.remove(arbiter.shapes[0])
    space.remove(arbiter.shapes[0].body, arbiter.shapes[0])

    # bullets.remove(arbiter.shapes[1])
    space.remove(arbiter.shapes[1].body, arbiter.shapes[1])


# pygame setup
pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# pymunk set up
space = pymunk.Space()
draw_options = pymunk.pygame_util.DrawOptions(WIN)

h = space.add_collision_handler(
    collision_types["asteroid"], collision_types["bullet"])

h.begin = asteroid_x_bullet


bullets = []
asteroids = []


frame = 0
while True:
    clock.tick(60)
    space.step(1/60)

    if frame == 0:
        # Spawn a ball
        ball = Ball((300, 300), 30, ASTEROID)

        ball.mass = 10
        ball.elasticity = 0.4
        ball.friction = 0.4
        ball.color = (255, 0, 0, 0)
        ball.collision_type = collision_types['asteroid']
        space.add(ball.body, ball)

        asteroids.append(ball)

        bullet = Bullet((20, 310), (40, 10), 5, BULLET)

        bullets.append(bullet)

        space.add(bullet.body, bullet.shape)
        # space.add(asteroid.body, asteroid.shape)
        bullet.shape.body.apply_impulse_at_local_point(
            (2000, 0), (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    WIN.fill((255, 255, 255))
    for x in bullets:
        x.draw(WIN)

    for x in asteroids:
        x.draw(WIN)

    # space.debug_draw(draw_options)
    pygame.display.flip()
    frame += 1
    if frame == 200:
        for x in bullets:
            space.remove(x.body, x)
        for x in asteroids:
            space.remove(x.body, x)
        frame = 0
