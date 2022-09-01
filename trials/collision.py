from calendar import timegm
import pygame
import sys


def bouncing_rect():
    global x_speed, y_speed, other_speed
    moving_rect.x += x_speed
    moving_rect.y += y_speed

    # collision with screen borders
    if moving_rect.right >= WIDTH or moving_rect.left <= 0:
        x_speed *= -1
    if moving_rect.bottom >= HEIGHT or moving_rect.top <= 0:
        y_speed *= -1

    # moving the other rectangle
    other_rect.y += other_speed
    if other_rect.top <= 0 or other_rect.bottom >= HEIGHT:
        other_speed *= -1

    # collision with rect
    collision_tolerance = 10
    if moving_rect.colliderect(other_rect):
        if abs(other_rect.top - moving_rect.bottom) < collision_tolerance and y_speed > 0:
            y_speed *= -1
        if abs(other_rect.bottom - moving_rect.top) < collision_tolerance and y_speed < 0:
            y_speed *= -1
        if abs(other_rect.left - moving_rect.right) < collision_tolerance and x_speed > 0:
            x_speed *= -1
        if abs(other_rect.right - moving_rect.left) < collision_tolerance and x_speed < 0:
            x_speed *= -1

    pygame.draw.rect(WIN, (255, 255, 255), moving_rect)
    pygame.draw.rect(WIN, (255, 0, 0), other_rect)


pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

moving_rect = pygame.Rect(350, 350, 100, 100)
x_speed, y_speed = 5, 4

other_rect = pygame.Rect(300, 600, 200, 100)
other_speed = 2


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    WIN.fill((30, 30, 30))
    bouncing_rect()
    pygame.display.flip()
    clock.tick(60)
