from machine import ADC, Pin

from .utils import scale_value

"""
potentiometer
from potentiometer import Potentiometer
potentiometer = Potentiometer(pin=36)
print(potentiometer.get_value_in_scale(out_scale_min=0, out_scale_max=100)
"""


class Potentiometer:
    adc = None

    def __init__(self, pin: int):
        self.adc = ADC(Pin(pin))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)

    def get_value(self):
        return self.adc.read()

    def get_value_in_scale(self, out_scale_min: float, out_scale_max: float):
        return scale_value(
            value=self.get_value(),
            in_min=0,
            in_max=4095,
            out_min=out_scale_min,
            out_max=out_scale_max,
        )
