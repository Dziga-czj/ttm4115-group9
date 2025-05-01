
import paho.mqtt.client as mqtt
import json


MQTT_BROKER = 'mqtt20.iik.ntnu.no'
MQTT_PORT = 1883


MQTT_SCOOTER = "ttm4115/group09/v3/scooter/"
MQTT_TOPIC_USER = 'ttm4115/escargot/user/'
MQTT_TOPIC_GENERAL = 'ttm4115/escargot/general'
MQTT_TOPIC_GENERAL_RESPONSE = 'ttm4115/escargot/general_response'

DEBUG = True

class User():
    def __init__(self):
        self.id = None
        self.username = None
        self.email = None
        self.tokens = None
        self.on_login = None
    



class Mqtt_client():

    def wait_for_answer(self, topic):
        while self.answer != None:
            self.mqtt_client.loop()

    def on_connect(self, client, userdata, flags, rc):
            # we just log that we are connected
            if DEBUG :
                print('MQTT connected to {}'.format(client))

    def on_message(self, client, userdata, msg):
        if DEBUG:
                print('Incoming message to topic {}'.format(msg.topic))

        try :
            payload = json.loads(msg.payload.decode("utf-8"))
        except:
            
            return
        
        if DEBUG:
            print(f"Stringified Payload {payload}")


        if msg.topic == MQTT_TOPIC_GENERAL:
            command = payload['command']
            if command == "success":

                print(f"Success with id {payload['id']}")
                id = payload['id']
                self.user.id = payload['id']
                self.user_topic = MQTT_TOPIC_USER + str(self.user.id)
                self.mqtt_client.subscribe(self.user_topic)
                self.mqtt_client.unsubscribe(MQTT_TOPIC_GENERAL)


        elif msg.topic == self.user_topic: 
            command = payload['command']
            match command:
                case "account_info":
                    self.user.username = payload['username']
                    self.user.email = payload['email']
                    self.user.tokens = payload['tokens']


                    

        else :
            None
          

    def send_message(self, topic, payload):
        if DEBUG:
            print(f"Sending message to topic {topic}")
        self.mqtt_client.publish(topic, payload=payload)

    def __init__(self):
        self.user = User()
        self.user_topic = None

        self.mqtt_client = mqtt.Client(callback_api_version = mqtt.CallbackAPIVersion.VERSION1)
        # callback methods
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
        self.mqtt_client.subscribe(MQTT_TOPIC_GENERAL)
        self.mqtt_client.loop_start()

    def stop(self):
        self.mqtt_client.loop_stop()


    def get_user_info(self):
        if self.user.username is not None:
            return self.user
        else:
            return None

    