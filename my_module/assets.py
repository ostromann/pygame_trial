import pygame
import os
from . import config

pygame.mixer.init()

sounds = {
    'bullet_fire': pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3')),
    'explosion': pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3')),
}

images = {
    'space': pygame.image.load(os.path.join('Assets', 'space.png')),
    'stars': pygame.image.load(os.path.join('Assets', 'stars.png')),
    'explosion': pygame.image.load(os.path.join('Assets', 'explosion.png')),
    'asteroid': pygame.image.load(os.path.join('Assets', 'asteroid.png')),
    'spaceship': pygame.image.load(os.path.join('Assets', 'spaceship.png')),
    'bullet': pygame.image.load(os.path.join('Assets', 'bullet.png')),
    'shield': pygame.image.load(os.path.join('Assets', 'shield.png')),
}

sprites = {
    'spaceship': os.path.join('Assets', 'spaceship_sprites.png'),
    'miscellaneous': os.path.join('Assets', 'SpaceShooterAssets', 'SpaceShooterAssetPack_Miscellaneous.png'),
    'spaceships': os.path.join('Assets', 'SpaceShooterAssets', 'SpaceShooterAssetPack_Ships.png'),
    'backgrounds': os.path.join('Assets', 'SpaceShooterAssets', 'SpaceShooterAssetPack_Backgrounds.png'),
    'ui': os.path.join('Assets', 'SpaceShooterAssets', 'SpaceShooterAssetPack_UI.png'),
    'projectile': os.path.join('Assets', 'SpaceShooterAssets', 'SpaceShooterAssetPack_Projectile.png'),
}
