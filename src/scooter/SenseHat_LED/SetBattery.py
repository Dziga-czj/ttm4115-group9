def setBattery(ledMatrix, R, G, Y, battery): # battery 1 - 8
    m = ledMatrix.copy()

    if 1 <= battery <= 2:
        for i in range(battery):
            m[56+i] = R
        
    if 2 <= battery <= 4:
        for i in range(battery):
            m[56+i] = Y
            
    if 5 <= battery <= 8:
        for i in range(battery):
            m[56+i] = G
            
    return m