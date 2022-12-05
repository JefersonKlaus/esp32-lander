from machine import Pin

from .utils import scale_value

"""
led bar
from led_bar import LedBar
led_bar = LedBar(pin_list=[15, 2, 0, 4, 5, 18, 19, 21, 22, 23])
led_bar.turn_on_in_scale(value=50, in_scale_min=0, in_scale_max=100)
"""


class LedBar:
    led_list = None

    def __init__(self, pin_list):
        self.led_list = list()

        for i in range(0, len(pin_list)):
            led = Pin(pin_list[i], Pin.OUT)
            led.value(0)
            self.led_list.append(led)

    def turn_off(self):
        for led in self.led_list:
            led.value(0)

    def turn_on_in_scale(self, value: float, in_scale_min: float, in_scale_max: float):
        led_position = int(
            scale_value(
                value=value,
                in_min=in_scale_min,
                in_max=in_scale_max,
                out_min=0,
                out_max=len(self.led_list),
            )
        )

        for i in range(0, led_position):
            led = self.led_list[i]
            led.value(1)

        if led_position < len(self.led_list):
            for i in range(led_position, len(self.led_list)):
                led = self.led_list[i]
                led.value(0)
