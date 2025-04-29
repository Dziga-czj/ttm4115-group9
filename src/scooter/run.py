from ScooterComponent import *
from SenseHat_LED.Display import *
from sense_hat import SenseHat

scooterID = 1 # 
broker = "mqtt20.iik.ntnu.no" # TBD
port = 1883 # TBD
sense = SenseHat()
sense.set_imu_config(True, True, True)


def run():
    scooter = ScooterLogic(ID=scooterID, broker=broker, port=port, battery=Battery(ID=scooterID, battery_level=8.0))
    display(sense, scooter.battery.get_battery)