import sys
import pygame as pg
from pygame.color import THECOLORS
import pymunk as pm


def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p[0]), int(-p[1]+600)


pg.init()
screen = pg.display.set_mode((600, 600))
clock = pg.time.Clock()

space = pm.Space()
space.gravity = (0.0, -900.0)

# Walls
static_body = space.static_body
static_lines = [
    pm.Segment(static_body, (111.0, 280.0), (407.0, 246.0), 0.0),
    pm.Segment(static_body, (407.0, 246.0), (407.0, 343.0), 0.0),
    pm.Segment(static_body, (111.0, 420.0), (407.0, 386.0), 0.0),
    pm.Segment(static_body, (407.0, 386.0), (407.0, 493.0), 0.0),
]
for idx, line in enumerate(static_lines):
    line.elasticity = 0.95
    if idx < 2:  # Lower lines.
        # The lower lines are in category 2, in binary 0b10.
        line.filter = pm.ShapeFilter(categories=2)
    else:  # Upper lines.
        # The upper lines are in category 1, in binary 0b1.
        line.filter = pm.ShapeFilter(categories=1)
space.add(static_lines)

balls = []
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            radius = 15 if event.button == 1 else 30
            mass = 10
            inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
            body = pm.Body(mass, inertia)
            body.position = to_pygame(event.pos)
            shape = pm.Circle(body, radius, (0, 0))
            shape.elasticity = 0.95
            if shape.radius > 25:
                # bin(pm.ShapeFilter.ALL_MASKS ^ 1) is '0b11111111111111111111111111111110'
                # That means all categories are checked for collisions except
                # bit 1 (the upper lines) which are ignored.
                shape.filter = pm.ShapeFilter(
                    mask=pm.ShapeFilter.ALL_MASKS ^ 1)
            else:
                # Ignores category bin(2), '0b11111111111111111111111111111101'
                # All categories are checked for collisions except bit 2 (the lower lines).
                shape.filter = pm.ShapeFilter(
                    mask=pm.ShapeFilter.ALL_MASKS ^ 2)

            space.add(body, shape)
            balls.append(shape)

    screen.fill(THECOLORS["white"])

    balls_to_remove = []
    for ball in balls:
        if ball.body.position.y < 100:
            balls_to_remove.append(ball)

        p = to_pygame(ball.body.position)
        if ball.radius > 25:
            color = THECOLORS["red"]
        else:
            color = THECOLORS["blue"]
        pg.draw.circle(screen, color, p, int(ball.radius), 2)

    for ball in balls_to_remove:
        space.remove(ball, ball.body)
        balls.remove(ball)

    for line in static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pg.draw.lines(screen, THECOLORS["gray29"], False, [p1, p2])

    # Update physics.
    dt = 1.0/60.0
    for x in range(1):
        space.step(dt)

    pg.display.flip()
    clock.tick(50)


pg.quit()
sys.exit()
