from ScooterComponent import *
from SenseHat_LED.Display import *
# from sense_hat import SenseHat

scooterID = 1 # can be string of any length, increace security
broker = "mqtt20.iik.ntnu.no" # TBD
port = 1883 # TBD
init_battery = 8.0


def run(): # with senseHat functions, only for pi with senseHat
    sense1 = SenseHat()
    sense1.set_imu_config(True, True, True)
    sense2 = SenseHat()
    sense2.set_imu_config(True, True, True)
    sense3 = SenseHat()
    sense3.set_imu_config(True, True, True)
    # one senseHat can only run one SenseHat(), three scooters required three senseHats
    scooter1 = Scooter(ID=1, 
                      broker=broker, 
                      port=port, 
                      senseHat=sense1, 
                      battery=Battery(ID=scooterID, battery_level=init_battery))
    scooter2 = Scooter(ID=2, 
                      broker=broker, 
                      port=port, 
                      senseHat=sense2, 
                      battery=Battery(ID=scooterID, battery_level=init_battery))
    scooter3 = Scooter(ID=3, 
                      broker=broker, 
                      port=port, 
                      senseHat=sense3, 
                      battery=Battery(ID=scooterID, battery_level=init_battery))

def run_test(): # same as run(), without senseHat functions, can be tested on pc
    scooter1 = Scooter_test(ID=1, 
                      broker=broker, 
                      port=port, 
                      battery=Battery(ID=scooterID, battery_level=init_battery))
    scooter2 = Scooter_test(ID=2, 
                      broker=broker, 
                      port=port, 
                      battery=Battery(ID=scooterID, battery_level=init_battery))
    scooter3 = Scooter_test(ID=3, 
                      broker=broker, 
                      port=port, 
                      battery=Battery(ID=scooterID, battery_level=init_battery))

run_test()
