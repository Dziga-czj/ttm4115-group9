from Scooter import Scooter

broker = "test.mosquitto.org" # TBD
port = 1883 # TBD

def run():
    scooter = Scooter(ID=1, broker=broker, port=port)