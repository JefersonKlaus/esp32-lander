import time

from machine import Pin, time_pulse_us

from .lengh import LenghtOptions


class Sonar:
    trig_pin = None
    echo_pin = None

    SOUND_VELOCITY = 340

    def __init__(self, pin_in, pin_out):
        """
        :param pin_in: ECHO default pin 14
        :param pin_out: TRIG default pin 13
        :return:
        """
        self.trig_pin = Pin(pin_out, Pin.OUT, 0)
        self.trig_pin.value(0)
        self.echo_pin = Pin(pin_in, Pin.IN, 0)

    def _send_pulse_and_wait(self, stabilize=False):
        if stabilize:
            self.trig_pin.value(0)  # Stabilize the sensor
            time.sleep_us(5)
        self.trig_pin.value(1)
        # Send a 10us pulse.
        time.sleep_us(10)
        self.trig_pin.value(0)
        try:
            pulse_time = time_pulse_us(self.echo_pin, 1, 500 * 2 * 30)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110:  # 110 = ETIMEDOUT
                raise OSError("Out of range")
            raise ex

    def distance_mm(self):
        pulse_time = self._send_pulse_and_wait()
        mm = pulse_time * 100 // 582
        return mm

    def distance_cm(self):
        pulse_time = self._send_pulse_and_wait()
        cms = (pulse_time / 2) / 29.1
        return cms
