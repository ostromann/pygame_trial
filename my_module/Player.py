from . import config


class Player():
    def __init__(self, number, ship):
        self.analog_keys = {}
        self.button_keys = {}
        self.ship = ship
        pass

    def handle_analog_input(self, event):
        # HANDLES ANALOG INPUTS
        print(self.analog_keys)
        # Horizontal Analog
        if abs(self.analog_keys[0]) > .1:
            if self.analog_keys[0] < -config.controller_deadzone:
                LEFT = True
            else:
                LEFT = False
            if self.analog_keys[0] > config.controller_deadzone:
                RIGHT = True
            else:
                RIGHT = False

        # Vertical Analog
        if abs(self.analog_keys[1]) > .1:
            if self.analog_keys[1] < -config.controller_deadzone:
                UP = True
            else:
                UP = False
            if self.analog_keys[1] > config.controller_deadzone:
                DOWN = True
            else:
                DOWN = False

        # Triggers
        if self.analog_keys[4] > 0:  # Left trigger
            color += 2
        if self.analog_keys[5] > 0:  # Right Trigger
            color -= 2

    def handle_button_presses(self, event):
        # Handle button presses
        if event.button == self.button_keys['left_arrow']:
            LEFT = True
        if event.button == self.button_keys['right_arrow']:
            RIGHT = True
        if event.button == self.button_keys['down_arrow']:
            DOWN = True
        if event.button == self.button_keys['up_arrow']:
            UP = True

    def handle_button_releases(self, event):
        # Handle button releases
        if event.button == self.button_keys['left_arrow']:
            LEFT = False
        if event.button == self.button_keys['right_arrow']:
            RIGHT = False
        if event.button == self.button_keys['down_arrow']:
            DOWN = False
        if event.button == self.button_keys['up_arrow']:
            UP = False
