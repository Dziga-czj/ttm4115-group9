def getSpeed(SenseHat, vx, vy, prev_ax, prev_ay, interval):
    accel = SenseHat.get_accelerometer_raw()
    print(accel)
    #alpha=0.5
    #ax = alpha*accel['x']+(1-alpha)*prev_ax
    #ay = alpha*accel['y']+(1-alpha)*prev_ay
    
    #prev_ax, prev_ay = ax, ay
    #vx += round(ax, 1) * 9.81 * interval
    #vy += round(ay, 1) * 9.81 * interval
    #print(ax, ay)
    
    
    ax = accel['x']
    ay = accel['y']
    
    vx = (ax-prev_ax)/interval
    vy = (ay-prev_ay)/interval
    
    prev_ax, prev_ay = ax, ay
    
    return vx, vy, prev_ax, prev_ay
    