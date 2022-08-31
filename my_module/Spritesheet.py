import pygame


class Spritesheet(pygame.sprite.Sprite):
    def __init__(self, filename, *groups):
        super().__init__(*groups)
        self.filename = filename
        self.spritesheet = pygame.image.load(filename).convert_alpha()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h), pygame.SRCALPHA)
        sprite.blit(self.spritesheet, (0, 0), (x*w, y, w, h))
        return sprite
