import base64
import cv2
import numpy as np
import paho.mqtt.client as mqtt

'''
    Still needs to be tested!!

    Mqtt node object that can send and recieve messages and images both ways
    Relative uses:
    - Both the pi and model run an instance of MqttNode 
    - Pi -> Image data -> model's image_stack
    - Use the image stack as the multithreading input stack
'''
class MqttNode():

    def __init__(self, client_id, broker, topic): 
        self.client = mqtt.Client(client_id=client_id)
        self.broker = broker
        self.topic = topic

        # Bind callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # Stack that stores all the inputs
        # For model w/ multithreading, treat MqttObj.input_stack as the input stack
        self.image_stack = []
        self.msg_stack = []

    def on_connect(self, client, userdata, flags, rc): #FOR ME: RC is the return code. If it is 0, connection is successful
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(self.topic)
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, message):
        '''
        Recieves a message. If it's an image, converts it into image format
        Appends the message to either the image or text stack
        '''
        payload = message.payload.decode("utf-8")
        flag = int(payload[0])
        content = payload[1:]
        if flag == 0:
            img_data = base64.b64decode(content)
            nparr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if frame is not None: 
                self.image_stack.append(frame)
                print("Image frame received")
        elif flag == 1:
            self.msg_stack.append(content)
            print("Text message received:", content)

    def send_message(self, message, type):
        '''
        Sends a message with mqtt client
        type = 0 for image
        type = 1 for string
        for image, message must be a numpy array
        '''
        if type == 0: 
            # Assume `message` is a cv2 image
            # Payload is the sent message, with 0 / 1 as the first character
            _, buffer = cv2.imencode('.jpg', message)
            b64_str = base64.b64encode(buffer).decode("utf-8")
            payload = '0' + b64_str
        elif type == 1: 
            payload = '1' + message
        else: 
            raise ValueError('Type of message not supported(use 0-image / 1-string)')
        
        self.client.publish(self.topic, payload)

    def connect(self):
        self.client.connect(self.broker)
        self.client.loop_start()

    def get_image_stack(self):
        return self.image_stack

    def get_msg_stack(self):
        return self.msg_stack
    
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

# EXAMPLE CODE: 
# from MqttNode import MqttNode
# import time

# client_id = "client_id"
# broker = "test.mosquitto.org"
# topic = "TEST"
# mqtt = MqttNode(client_id, broker, topic)

# mqtt.connect()

# mqtt.client.loop_start()
# while(True):
#     message = 'bob'
#     mqtt.send_message(message, 1)
#     print('sent message!')
#     time.sleep(10)