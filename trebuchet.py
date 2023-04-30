# import board
# import pwmio
# from adafruit_motor import servo
# import time

# # set up a servo on CPB pin A2
# pwm = pwmio.PWMOut(board.GP15, frequency=50)
# # Change min_pulse / max_pulse values to calibrate servo arm in either direction.
# # min ~ 500, max ~ 2500. Defaults are below & can be eliminated.
# servo_1 = servo.Servo(pwm, min_pulse=750, max_pulse=2250)

# # set angle (range can be from 0 to 180 - this is 180)
# servo_1.angle = 0

# while True:
#     # servo_1.angle = 20

import board
import time
import pwmio
from adafruit_motor import servo
import os
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import board
import pwmio
from adafruit_motor import servo
import board
import time
import pwmio
from adafruit_motor import servo


# create a PWMOut object on singla pins for servos.
pwm_left = pwmio.PWMOut(board.GP15, frequency=50)
pwm_right = pwmio.PWMOut(board.GP14, frequency=50)
# Create servo objects,.
servo_wind = servo.ContinuousServo(pwm_left)
servo_trigger = servo.ContinuousServo(pwm_right)

# To go forward or backward, just set throttle property on the servo. 1.0 is full throttle. 0.0 is full
# stop. Note that servo might not move if it's much lower than 0.5
# servo_left.throttle = 1.0
# servo_right.throttle = -1.0


print(f"Connecting to Wifi")
wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
# wifi.radio.connect(os.getenv("x"), os.getenv("y"))
print("Connected!")

pool = socketpool.SocketPool(wifi.radio)

aio_username = os.getenv("AIO_USERNAME")
aio_key = os.getenv("AIO_KEY")

servo_feed = aio_username + "/feeds/servo_feed"


def connected(client, userdata, flags, rc):
    print("Connected to Adafruit IO. Listening for topic changes in subscribed feeds.")
    client.subscribe(servo_feed)


def disconnected(client, userdata, rc):
    print("Disconneceted from Adafruit IO.")


def message(client, topic, message):
    print(f"topic: {topic},  message: {message}")
    if topic == servo_feed:
        print(message)
        if message == "stopwinch":
            servo_wind.throttle = 0
            time.sleep(0.2)
        elif message == "tighten":
            servo_wind.throttle = 0.4
            time.sleep(0.2)
        elif message == "loosen":
            servo_wind.throttle = -0.4
            time.sleep(0.2)
        elif message == "pull trigger":
            servo_trigger.throttle = 0.4
            time.sleep(0.2)
        elif message == "reset trigger":
            servo_trigger.throttle = -0.4
            time.sleep(0.2)
        elif message == "stoptrigger":
            servo_trigger.throttle = 0
            time.sleep(0.2)
        elif message == "0":
            time.sleep(0.2)


mqtt_client = MQTT.MQTT(
    broker=os.getenv("BROKER"),
    port=os.getenv("PORT"),
    username=aio_username,
    password=aio_key,
    socket_pool=pool,
    ssl_context=ssl.create_default_context()
)

mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

print("Connecting to Adafruit IO")
mqtt_client.connect()
# mqtt_client.publish(strip_on_off_feed + "/get", "")
# mqtt_client.publish(color_feed + "/get", "")
# mqtt_client.publish(servo_feed + "/get", "")

while True:
    mqtt_client.loop()

# mac_address = [f"{i:02x}" for i in wifi.radio.mac_address]
# print(':'.join(mac_address))
