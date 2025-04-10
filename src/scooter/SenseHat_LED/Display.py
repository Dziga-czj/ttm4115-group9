#need test on pi
import time
from sense_hat import SenseHat
from GetSpeed import getSpeed
from SetNumber import setNumber
from SetBattery import setBattery

sense = SenseHat()
sense.set_imu_config(True, True, True)


def display(SenseHat, speed, battery):
    
    R = [255, 0, 0]  # Red
    O = [0, 0, 0]
    G = [0, 255, 0]  # Green
    Y = [255, 255, 0] # Yellow
    ledMatrix = [
    O, O, O, R, O, O, O, R,
    O, O, O, O, O, O, O, O,
    O, O, O, R, O, O, O, R,
    O, O, O, O, O, O, O, O,
    O, O, O, R, O, O, O, R,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O #last line for battery
    ] 
    interval = 0.1
    vx = 0
    vy = 0
    
    while True:
        vx, vy = getSpeed(SenseHat, vx, vy, interval)
        speed = round((vx**2 + vy**2)**0.5)
        ones = speed % 10
        tens = speed // 10
        m = setBattery(setNumber(setNumber(ledMatrix, R, ones, True), R, tens), R, G, Y, battery)
        
        SenseHat.set_pixels(m)
        time.sleep(interval)
        
    



