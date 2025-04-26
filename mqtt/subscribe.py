import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc): #FOR ME: RC is the return code. If it is 0, connection is successful
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe("TEST")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, message):
    print("Message received:", str(message.payload.decode("utf-8")))

mqttBroker = "mqtt.eclipseprojects.io"

client = mqtt.Client(client_id="Message_Receiver")

client.on_connect = on_connect
client.on_message = on_message

print("Trying to connect to broker...")
client.connect(mqttBroker)

client.loop_forever()