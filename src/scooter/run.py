from ScooterComponent import *
from SenseHat_LED.Display import *
# from sense_hat import SenseHat

scooterID = 1 # 
broker = "mqtt20.iik.ntnu.no" # TBD
port = 1883 # TBD
# sense = SenseHat()
# sense.set_imu_config(True, True, True)
init_battery = 8.0


# def run():
#     scooter = Scooter(ID=scooterID, 
#                       broker=broker, 
#                       port=port, 
#                       senseHat=sense, 
#                       battery=Battery(ID=scooterID, battery_level=init_battery))

# run()

def run_test():
    scooter = Scooter_test(ID=scooterID, 
                      broker=broker, 
                      port=port, 
                      battery=Battery(ID=scooterID, battery_level=init_battery))

run_test()
