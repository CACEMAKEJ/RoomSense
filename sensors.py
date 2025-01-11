import os
import time, threading
import requests
import json
import adafruit_dht
import board
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from dotenv import load_dotenv  # Import dotenv

load_dotenv()


# this will print out the subscription status to console
class Listener(SubscribeListener):
    def status(self, pubnub, status):
        print(f'Status: \n{status.category.name}')


# here we create configuration for our pubnub instance
config = PNConfiguration()
SUBSCRIBE_KEY = os.getenv('SUBSCRIBE_KEY')
PUBLISH_KEY = os.getenv('PUBLISH_KEY')
USER_ID = os.getenv('USER_ID')
config.enable_subscribe = True
config.daemon = True

my_channel = "RoomTemp"
sensorList = ["DHT"]

pubnub = PubNub(config)
pubnub.add_listener(Listener())

def my_publish_callback(envelope, status):
    #Check whether request successfully completed or not
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
            #pubnub.publish().channel(my_channel).message('Connected to PubNub').pn_async(my_publish_callback)
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

# Initialize the DHT sensor on GPIO pin D4
dht_device = adafruit_dht.DHT22(board.D4)

alive = 0
data = {}

def temperatureCheck():
    # Maximum number of retries for reading data
    MAX_RETRIES = 5
    while True:
        success = False
        retries = 0

        while not success and retries < MAX_RETRIES:
            try:
                # Attempt to read temperature and humidity
                temperature_c = dht_device.temperature
                humidity = dht_device.humidity

                if temperature_c is not None and humidity is not None:
                    # If values are successfully retrieved, print them
                    print("Temp: {:.1f} C Humidity: {:.1f}%".format(temperature_c, humidity))
                    publish(my_channel, {"temperature": temperature_c})
                    success = True
                else:
                    # Retry if the sensor returned None
                    retries += 1
                    time.sleep(2.0)

            except RuntimeError as err:
                # Handle runtime errors
                retries += 1
                time.sleep(2.0)

        # Wait before attempting the next reading
        time.sleep(5.0)

if __name__ == '__main__':
    sensorsThread = threading.Thread(target=temperatureCheck)
    sensorsThread.start()
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(my_channel).execute()

