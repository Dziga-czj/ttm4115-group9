
import paho.mqtt.client as mqtt
import json
import database_manager
from argon2 import PasswordHasher
ph = PasswordHasher()


MQTT_BROKER = 'mqtt20.iik.ntnu.no'
MQTT_PORT = 1883

MQTT_TOPIC_INPUT = 'ttm4115/escargot/general'
MQTT_TOPIC_OUTPUT = 'ttm4115/escargot/general_response'

DEBUG = True

class Server():

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
        
        command = payload['command']
        match command:

            case "register":
                if DEBUG :
                    print(f"Command: {command}")
                username = payload['username']
                email = payload['email']
                password = payload['password']
                hashed = ph.hash(password)
                # Add user to database
                database_manager.add_user(username, email, hashed)
                # Send response
                response = {
                    'command': 'success',
                    'message': f'User {username} added successfully.',
                    'id': f'{database_manager.get_user_id(username)}'
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
                
            case "delete_account":
                if DEBUG:
                    print(f"Command: {command}")
                user_id = payload['user_id']
                # Delete account, there should be a verification step here before the user is deleted
                database_manager.delete_account(user_id)
                # Send response
                response = {
                    'status': 'success',
                    'message': f'Account with user ID {user_id} deleted successfully.'
                }
                self.mqtt_client.publish(MQTT_TOPIC_OUTPUT, payload=json.dumps(response))

            case "forgot_password":
                if DEBUG:
                    print(f"Command: {command}")
                email = payload['email']
                # Handle forgot password
                reset_token = database_manager.forgot_password(email)
                # Send response
                response = {
                    'status': 'success',
                    'message': f'Password reset token generated for {email}.',
                    'reset_token': reset_token
                }
                self.mqtt_client.publish(MQTT_TOPIC_OUTPUT, payload=json.dumps(response))

            case "change_password":
                if DEBUG:
                    print(f"Command: {command}")
                user_id = payload['user_id']
                new_password = payload['new_password']
                hashed = ph.hash(new_password)
                # Change password
                database_manager.change_password(user_id, hashed)
                # Send response
                response = {
                    'status': 'success',
                    'message': f'Password changed successfully for user ID {user_id}.'
                }
                self.mqtt_client.publish(MQTT_TOPIC_OUTPUT, payload=json.dumps(response))
            
            case _:
                if DEBUG :
                    print(f"Unknown command: {command}")


    def __init__(self):
        self.mqtt_client = mqtt.Client(callback_api_version = mqtt.CallbackAPIVersion.VERSION1)
        # callback methods
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
        self.mqtt_client.subscribe(MQTT_TOPIC_INPUT)
        self.mqtt_client.loop_start()

    def stop(self):
        self.mqtt_client.loop_stop()

s = Server()

try:
    while True:
        None
        
except KeyboardInterrupt:
    s.stop()
    print("\nExiting...")
    