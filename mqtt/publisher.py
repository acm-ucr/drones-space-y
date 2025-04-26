import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
import datetime


mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client(client_id="Message Sender", callback_api_version=2)
client.connect(mqttBroker)

while True:
    message = "Hello! This is a test message!"
    client.publish("TEST", message)
    print(f"Just published! Time: {datetime.datetime.now()}")
    time.sleep(10)