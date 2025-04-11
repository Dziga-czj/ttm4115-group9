def getSpeed(SenseHat, vx, vy, interval):
    accel = SenseHat.get_accelerometer_raw()
    ax = accel['x'] * 9.81
    ay = accel['y'] * 9.81
        
    vx += ax * interval
    vy += ay * interval
    
    return vx, vy
    