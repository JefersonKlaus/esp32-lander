import _thread
import json
import random
import time

from machine import reset

from esp_libs.mqtt import MQTTClient
from esp_libs.network import Network
from esp_libs.sonar import Sonar
from spaceship import Spaceship, SpaceshipCommand

SSID_ROUTER = "SSID"
PASSWORD_ROUTER = "PASSWORD"

BROKER_SERVER = "192.168.2.108"
TOPIC_SUBSCRIBE = b"spaceship/commands"
TOPIC_STATUS_HARDWARE = b"status/hardware"


def subscri_callback(topic, msg):
    command = msg.decode("utf-8")
    if command == "LAND":
        print("LAND")
        spaceship.land()

    elif command == "TAKE_OFF":
        print("TAKE_OFF")
        spaceship.takeoff()


def get_network_connection():
    network = Network()
    network.sta_setup(ssid_router=SSID_ROUTER, password_router=PASSWORD_ROUTER)

    while not network.sta_connection.isconnected():
        pass

    return network


def get_mqtt_connection():
    client = MQTTClient(
        client_id="esp32-id-" + str(random.randint(0, 1000)),
        server=BROKER_SERVER,
        keepalive=60,
    )
    client.set_callback(subscri_callback)
    client.connect()
    client.subscribe(topic=TOPIC_SUBSCRIBE)
    return client


def check_msg(client):
    while True:
        time.sleep(1)
        lock.acquire()
        try:
            print("check_msg")
            client.check_msg()
            client.ping()
        except Exception as error:
            print("check_msg error")
            print(error)
            client = get_mqtt_connection()
            pass

        lock.release()


def public_status():
    while True:
        time.sleep(5)

        lock.acquire()
        try:
            print("public_status")
            spaceship.generate_mqtt_log()
        except Exception as error:
            print("public_status error")
            print(error)
            pass

        lock.release()


def main():
    _thread.start_new_thread(check_msg, (client,))
    _thread.start_new_thread(public_status, ())

    while True:
        try:
            time.sleep(1)
        except OSError as e:
            print("Failed to connect to MQTT broker. Restarting machine...")
            time.sleep(2)
            reset()
        except:
            print("Device needs to be reseted")


lock = _thread.allocate_lock()
network = get_network_connection()
client = get_mqtt_connection()

spaceship = Spaceship(pin_engine=2, pin_sonar_in=14, pin_sonar_out=13)
spaceship.enable_mqtt_logs(client=client, topic=TOPIC_STATUS_HARDWARE)

if __name__ == "__main__":
    main()
