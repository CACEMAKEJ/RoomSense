import os
import time, threading
import requests
import json
import adafruit_dht
import digitalio
import board
import RPi.GPIO as GPIO
from dotenv import load_dotenv
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

load_dotenv()

class Listener(SubscribeListener):
    def status(self, pubnub, status):
        print(f'Status: \n{status.category.name}')


config = PNConfiguration()
SUBSCRIBE_KEY = os.getenv('SUBSCRIBE_KEY')
PUBLISH_KEY = os.getenv('PUBLISH_KEY')
USER_ID = os.getenv('USER_ID')
config.subscribe_key = SUBSCRIBE_KEY
config.publish_key = PUBLISH_KEY
config.enable_subscribe = True
config.daemon = True
config.uuid = USER_ID

print(f"SUBSCRIBE_KEY: {SUBSCRIBE_KEY}")
print(f"PUBLISH_KEY: {PUBLISH_KEY}")
print(f"USER_ID: {USER_ID}")

my_channel = "RoomTemp"
sensorList = ["DHT"]

pubnub = PubNub(config)
pubnub.add_listener(Listener())

def my_publish_callback(envelope, status):
    if not status.is_error():
        pass
    else:
        pass

class MySubscribeCallback(SubscribeCallback):
    def presense(self, pubnub, presence):
        pass

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass
        elif status.category == PNStatusCategory.PNConnectedCategory:
            print("Connected to channel")
            pass
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass

    def message(self, pubnub, message):
        print(message.message)
        received = message.message
        if "temperature" in received.keys():
            if received["temperature"]:
                data["temperature"] = received["temperature"]
            else:
                print("no data")


pubnub.subscribe().channels(my_channel).execute()

def publish(channel, message):
    pubnub.publish().channel(channel).message(message).pn_async(my_publish_callback)

dht_device = adafruit_dht.DHT22(board.D4)

alive = 0
data = {}
currentTemp = 15

def temperatureCheck():
    global currentTemp
    MAX_RETRIES = 5
    while True:
        success = False
        retries = 0

        while not success and retries < MAX_RETRIES:
            try:
                temperature_c = dht_device.temperature
                humidity = dht_device.humidity

                if temperature_c is not None and humidity is not None:
                    print("Temp: {:.1f} C Humidity: {:.1f}%".format(temperature_c, humidity))
                    currentTemp = temperature_c
                    publish(my_channel, {"temperature": temperature_c, "humidity" : humidity})
                    success = True
                else:
                    retries += 1
                    time.sleep(2.0)

            except RuntimeError as err:
                retries += 1
                time.sleep(2.0)

      
        time.sleep(5.0)



led = digitalio.DigitalInOut(board.D16)  
led.direction = digitalio.Direction.OUTPUT

def ledControl():
    while True:
        if currentTemp > 28:
            led.value = True  # Turn LED on
            publish(my_channel, {"lightStatus": "ON"})
            time.sleep(5)
        else:
            led.value = False  # Turn LED off
            publish(my_channel, {"lightStatus": "OFF"})
            time.sleep(5)




if __name__ == '__main__':
    temperatureCheckThread = threading.Thread(target=temperatureCheck)
    temperatureCheckThread.start()
    ledThread = threading.Thread(target=ledControl)
    ledThread.start()

    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(my_channel).execute()

