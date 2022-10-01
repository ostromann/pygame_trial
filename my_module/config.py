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
scale = 2
# 256, 128 # 512, 256  # 1400, 700

display_w, display_h = 512 * scale, 256 * scale
main_w, main_h = display_w / 4, display_h
left_w, left_h = display_w / 2, display_h
right_w, right_h = display_w / 4, display_h

spaceship_size = (16*scale, 16*scale)
spaceship_mass = 10
asteroid_density = 0.0015
explosion_timeout = 4*4

controller_deadzone = 0.2

# keybindings
keys = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'shoot': pygame.K_SPACE
}
