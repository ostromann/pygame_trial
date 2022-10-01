import math
from . import utils
from . import config

'''TODO:
Make all item- or sprite-like classes a subclass of this class which handles all drawing etc.'''


class MyDrawableObject():
    # TODO

    def draw(self, win):
        angle = math.degrees(-self._get_body().angle)
        x_offset = self.size[0] / 2
        y_offset = self.size[1] / 2
        x, y = self._get_body().position

        utils.blitRotate2(win, self.image, (x-x_offset, y-y_offset), angle)

    def is_out_of_bounds(self):
        x, y = self._get_body().position
        if x < 0 or x > config.screen_width:
            return True
        if y < 0 or y > config.screen_height:
            return True
        return False
