import os

collision_types = {
    "bullet": 1,
    "asteroid": 2,
    "ship": 3,
    "item": 4,
}

fps = 30
dt = 1/fps

screen_width, screen_height = 1400, 700  # 900, 500


asteroid_density = 0.0015

# BULLET_FIRE_SOUND = pygame.mixer.Sound(
#     os.path.join('Assets', 'Gun+Silencer.mp3'))

bullet_fire_sound = os.path.join('Assets', 'Gun+Silencer.mp3')
