# test on pi, show the realtime speed and battery level on the led matrix
import time
from GetSpeed import getSpeed
from SetNumber import setNumber
from SetBattery import setBattery
from sense_hat import SenseHat

sense = SenseHat()

def display(SenseHat, battery):
    
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
    prev_ax=0
    prev_ay=0
    
    accum = 0
    prev_accum = accum // 3
    
    
    
    # simulate the battery runs out by time,  from 8 to 0
    while True:
        if battery <= 0:
            sense.show_message("No Battery", text_colour=[255, 0, 0])
            break
        accum +=1
        if prev_accum < accum // 1:
            battery -= 0.1
            prev_accum = accum // 1
        speed = round((vx**2 + vy**2)**0.5)
        print("v=", speed)
        ones = speed % 10
        tens = speed // 10
        m = setBattery(setNumber(setNumber(ledMatrix, R, ones, True), R, tens), R, G, Y, battery)
        SenseHat.set_pixels(m)
        time.sleep(interval)
        vx, vy, prev_ax, prev_ay = getSpeed(SenseHat, vx, vy, prev_ax, prev_ay, interval)
        
            
        
        
# display(sense,8.0)
    



