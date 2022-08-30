import math
from . import config


class Background():
    def __init__(self, image, scroll_speed, base_layer=False):
        self.image = image.convert() if base_layer else image.convert_alpha()
        self.tiles = math.ceil(config.screen_width /
                               self.image.get_width()) + 1
        self.scroll_speed = scroll_speed
        self.scroll = 0

    def draw(self, win):
        # draw scrolling background
        for i in range(0, self.tiles):
            win.blit(self.image, (i * self.image.get_width() + self.scroll, 0))

        # scroll background
        self.scroll += self.scroll_speed

        # reset scroll
        if abs(self.scroll) > self.image.get_width():
            self.scroll = 0
