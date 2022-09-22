import os
import pygame

collision_types = {
    "bullet": 1,
    "asteroid": 2,
    "spaceship": 3,
    "item": 4,
}

object_categories = {
    "player":           0b0001,
    "player_bullet":    0b0010,
    "asteroid":         0b0100,
    "item":             0b1000,
}

category_masks = {
    "player":           0b1100,
    "player_bullet":    0b1100,
    "asteroid":         0b1111,
    "item":             0b1101
}

fps = 30
dt = 1/fps
scale = 4
# 256, 512  # 128, 256  # 900, 500  # 1400, 700
screen_width, screen_height = 128 * scale, 256 * scale

spaceship_size = (8*scale, 8*scale)
spaceship_mass = 10
asteroid_density = 0.0015
explosion_timeout = 4*4

# keybindings
keys = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'shoot': pygame.K_SPACE
}
