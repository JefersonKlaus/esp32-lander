from machine import ADC, Pin

from .utils import scale_value

"""
joystick
from joystick import Joystick
joystick = Joystick(pin_x=36, pin_y=39, pin_z=14)
print(joystick.get_x_value())
print(joystick.get_y_value())
print(joystick.get_z_value())
"""


class Joystick:
    x_val = None
    y_val = None
    z_val = None

    out_min = -10
    out_max = 10

    def __init__(self, pin_x: int, pin_y: int, pin_z: int):
        self.x_val = ADC(Pin(pin_x, Pin.IN))
        self.y_val = ADC(Pin(pin_y, Pin.IN))
        self.z_val = Pin(pin_z, Pin.IN, Pin.PULL_UP)

        self.x_val.atten(ADC.ATTN_11DB)
        self.y_val.atten(ADC.ATTN_11DB)
        self.x_val.width(ADC.WIDTH_12BIT)
        self.y_val.width(ADC.WIDTH_12BIT)

    def set_scale(self, out_min, out_max):
        self.out_min = out_min
        self.out_max = out_max

    def get_x_value(self):
        return scale_value(
            value=self.x_val.read(),
            in_min=0,
            in_max=4095,
            out_min=self.out_min,
            out_max=self.out_max,
        )

    def get_y_value(self):
        return scale_value(
            value=self.y_val.read(),
            in_min=0,
            in_max=4095,
            out_min=self.out_min,
            out_max=self.out_max,
        )

    def get_z_value(self):
        return 1 if 0 == self.z_val.value() else 0
