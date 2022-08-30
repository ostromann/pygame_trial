import os
import pygame

collision_types = {
    "bullet": 1,
    "asteroid": 2,
    "ship": 3,
    "item": 4,
}


fps = 30
dt = 1/fps
screen_width, screen_height = 1400, 700  # 900, 500  # 1400, 700

asteroid_density = 0.0015
explosion_timeout = 5

# keybindings
keys = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'shoot': pygame.K_SPACE
}
