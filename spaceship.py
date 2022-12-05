import _thread
import json
import time

from machine import Pin

from esp_libs.lengh import LenghtOptions
from esp_libs.sonar import Sonar


class SpaceshipCommand:
    NONE = "NONE"
    ABORT = "ABORT"
    LAND = "LAND"
    TAKE_OFF = "TAKE OFF"


class SpaceshipStatus:
    LANDING = "LANDING"
    LANDED = "LANDED"
    TAKING_OFF = "TAKING OFF"
    FLYING = "FLYING"
    ABORT = "ABORTING"
    OFF = "OFF"


class Spaceship:
    device_engine = None
    device_sonar = None

    spaceship_command = SpaceshipCommand.NONE

    status_engine = False
    status_altitude = 0
    status_spaceship = SpaceshipStatus.OFF

    mqtt_client = None
    mqtt_topic = None

    def __init__(self, pin_engine=2, pin_sonar_in=14, pin_sonar_out=13):
        self.device_engine = Pin(pin_engine, Pin.OUT)
        self.device_sonar = Sonar(pin_in=pin_sonar_in, pin_out=pin_sonar_out)

    def get_altitude(self):
        _status_altitude = self.device_sonar.distance_mm()
        if _status_altitude > -1:
            self.status_altitude = _status_altitude
        return self.status_altitude

    def turn_on_engine(self):
        self.status_engine = True
        self.device_engine.value(1)

    def turn_off_engine(self):
        self.status_engine = False
        self.device_engine.value(0)

    def get_status(self):
        return {
            "engine": "ON" if self.status_engine else "OFF",
            "command": self.spaceship_command,
            "status": self.status_spaceship,
            "altitude": self.get_altitude(),
        }

    def land(self):
        if self.spaceship_command == SpaceshipCommand.LAND:
            print("Spaceship - land: Landing already in progress")
            return

        print("Spaceship - land: Landing started")
        self.status_spaceship = SpaceshipStatus.LANDING
        self.spaceship_command = SpaceshipCommand.LAND

        self.generate_mqtt_log()

        _last_positions = []
        while True:
            if self.spaceship_command != SpaceshipCommand.LAND:
                self.turn_off_engine()
                break

            self.status_altitude = self.get_altitude()

            # get last 3 positions to be sure that the value is true
            _last_positions.append(self.status_altitude)
            if len(_last_positions) > 3:
                _last_positions.pop(0)

            print("Spaceship - land: ALTITUDE => " + str(self.status_altitude))
            print(
                "Spaceship - land: ALTITUDE M => "
                + str(sum(_last_positions) / len(_last_positions))
            )

            if sum(_last_positions) / len(_last_positions) >= 26:
                self.turn_on_engine()
            else:
                self.turn_off_engine()
                break

            self.generate_mqtt_log()
            time.sleep(0.5)

        if self.spaceship_command == SpaceshipCommand.LAND:
            self.status_spaceship = SpaceshipStatus.LANDED
            self.spaceship_command = SpaceshipCommand.NONE
            print("Spaceship - land: Landing finished")
        else:
            print("Spaceship - land: Aborted Landing")

        self.generate_mqtt_log()

    def takeoff(self):
        if self.spaceship_command == SpaceshipCommand.TAKE_OFF:
            print("Spaceship - takeoff: Takeoff already in progress")
            return

        print("Spaceship - takeoff: Takeoff started")
        self.status_spaceship = SpaceshipStatus.TAKING_OFF
        self.spaceship_command = SpaceshipCommand.TAKE_OFF

        self.generate_mqtt_log()

        _last_positions = []
        while True:
            if self.spaceship_command != SpaceshipCommand.TAKE_OFF:
                self.turn_off_engine()
                break

            self.status_altitude = self.get_altitude()

            # get last 3 positions to be sure that the value is true
            _last_positions.append(self.status_altitude)
            if len(_last_positions) > 3:
                _last_positions.pop(0)

            print("Spaceship - take_off: ALTITUDE => " + str(self.status_altitude))
            print(
                "Spaceship - land: ALTITUDE M => "
                + str(sum(_last_positions) / len(_last_positions))
            )

            if sum(_last_positions) / len(_last_positions) <= 300:
                self.turn_on_engine()
            else:
                self.turn_off_engine()
                break

            self.generate_mqtt_log()
            time.sleep(0.5)

        if self.spaceship_command == SpaceshipCommand.TAKE_OFF:
            self.status_spaceship = SpaceshipStatus.FLYING
            self.spaceship_command = SpaceshipCommand.NONE
            print("Spaceship - take_off: Takeoff finished")
        else:
            print("Spaceship - take_off: Aborted takeoff")

        self.generate_mqtt_log()

    def abort_operation(self):
        if self.spaceship_command == SpaceshipCommand.ABORT:
            print("Spaceship - abort_operation: Abortion already in progress")
            return

        if self.spaceship_command == SpaceshipCommand.NONE:
            print("Spaceship - abort_operation: No operation running")
            return

        if self.spaceship_command == SpaceshipCommand.LAND:
            print("Spaceship - abort_operation: Aborting landing")

        if self.spaceship_command == SpaceshipCommand.TAKE_OFF:
            print("Spaceship - abort_operation: Aborting takeoff")

        self.status_spaceship = SpaceshipStatus.ABORT
        self.spaceship_command == SpaceshipCommand.ABORT

    def enable_mqtt_logs(self, client, topic):
        self.mqtt_client = client
        self.mqtt_topic = topic

    def generate_mqtt_log(self):
        if self.mqtt_topic and self.mqtt_client:
            self.mqtt_client.publish(
                topic=self.mqtt_topic,
                msg=json.dumps(self.get_status()),
                qos=0,
            )
