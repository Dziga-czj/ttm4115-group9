
import paho.mqtt.client as mqtt
import json
import database_manager

MQTT_BROKER = 'mqtt20.iik.ntnu.no'
MQTT_PORT = 1883

MQTT_TOPIC_INPUT = 'ttm4115/escargot/friends'
MQTT_TOPIC_OUTPUT = 'ttm4115/escargot/friends_answer'

DEBUG = True

def on_connect(self, client, userdata, flags, rc):
        # we just log that we are connected
        if DEBUG :
            print('MQTT connected to {}'.format(client))

def on_message(self, client, userdata, msg):
    """
    Processes incoming MQTT messages.

    We assume the payload of all received MQTT messages is an UTF-8 encoded
    string, which is formatted as a JSON object. The JSON object contains
    a field called `command` which identifies what the message should achieve.

    As a reaction to a received message, we can for example do the following:

    * create a new state machine instance to handle the incoming messages,
    * route the message to an existing state machine session,
    * handle the message right here,
    * throw the message away.

    """
    if DEBUG:
        print('Incoming message to topic {}'.format(msg.topic))


    try :
        payload = json.loads(msg.payload.decode("utf-8"))
    except:
        
        return
    
    if DEBUG:
        print(f"Stringified Payload {payload}")
    
    command = payload['command']
    match command:

        case "add_user":
            if DEBUG :
                print(f"Command: {command}")
            username = payload['username']
            email = payload['email']
            password = payload['password']
            # Add user to database
            database_manager.add_user(username, email, password)
            # Send response
            response = {
                'status': 'success',
                'message': f'User {username} added successfully.'
            }
            self.mqtt_client.publish(MQTT_TOPIC_OUTPUT, payload=json.dumps(response))

        case "send_friend_request":
            if DEBUG :
                print(f"Command: {command}")
            user_id = payload['user_id']
            friend_id = payload['friend_id']
            # Send friend request
            database_manager.send_friend_request(user_id, friend_id)
            # Send response
            response = {
                'status': 'success',
                'message': f'Friend request sent from {user_id} to {friend_id}.'
            }
            self.mqtt_client.publish(MQTT_TOPIC_OUTPUT, payload=json.dumps(response))

        case "accept_friend_request":
            if DEBUG :
                print(f"Command: {command}")
            user_id = payload['user_id']
            friend_id = payload['friend_id']
            # Accept friend request
            database_manager.accept_friend_request(user_id, friend_id)
            # Send response
            response = {
                'status': 'success',
                'message': f'Friend request accepted from {friend_id} by {user_id}.'
            }
            self.mqtt_client.publish(MQTT_TOPIC_OUTPUT, payload=json.dumps(response))
        
        case "reject_friend_request":
            if DEBUG :
                print(f"Command: {command}")
            user_id = payload['user_id']
            friend_id = payload['friend_id']
            # Accept friend request
            database_manager.reject_friend_request(user_id, friend_id)
            # Send response
            response = {
                'status': 'success',
                'message': f'Friend request rejected from {friend_id} by {user_id}.'
            }
            self.mqtt_client.publish(MQTT_TOPIC_OUTPUT, payload=json.dumps(response))


        #case "new_timer":
        #    if DEBUG :
        #        print(f"Command: {command}")
        #    name = payload['name']
        #    duration = payload['duration']
        #    duration = int(duration)

        #case "cancel_timer":
        #    if DEBUG :
        #        print(f"Command: {command}")
        #    name = payload['name']

        #    self.mqtt_client.publish(MQTT_TOPIC_OUTPUT, payload=str)

        #case "status_single_timer":
        #    if DEBUG :
        #        print(f"Command: {command}")
        #    name = payload['name']
        
        case _:
            if DEBUG :
                print(f"Unknown command: {command}")


def run_server():

    mqtt_client = mqtt.Client()
    # callback methods
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    mqtt_client.subscribe(MQTT_TOPIC_INPUT)
    mqtt_client.loop_start()