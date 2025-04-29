import math
def setBattery(ledMatrix, R, G, Y, battery): # battery 0.0 - 8.0
    m = ledMatrix.copy()

    if 0 <= battery < 0.5: # empty
        return m

    if 0.5 <= battery < 2.5: # 0.5， 1.4， 1.5， 2.4
        for i in range(math.floor(battery+0.5)):
            m[56+i] = R
        
    if 2.5 <= battery < 5.5:
        for i in range(math.floor(battery+0.5)):
            m[56+i] = Y
            
    if 5.5 <= battery <= 8:
        for i in range(math.floor(battery+0.5)):
            m[56+i] = G
            
    return m