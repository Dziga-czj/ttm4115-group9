def setNumber(ledMatrix, R, n, ones=False): # R is color
    m = ledMatrix.copy()
    x = 4 if ones else 0
    
    if n == 1:
        m[11+x] = R
        m[27+x] = R
    if n == 2:
        m[1+x] = R
        m[2+x] = R
        m[11+x] = R
        m[17+x] = R
        m[18+x] = R
        m[25+x] = R
        m[33+x] = R
        m[34+x] = R
    if n == 3:
        m[1+x] = R
        m[2+x] = R
        m[11+x] = R
        m[17+x] = R
        m[18+x] = R
        m[27+x] = R
        m[33+x] = R
        m[34+x] = R
    if n == 4:
        m[1+x] = R
        m[9+x] = R
        m[11+x] = R
        m[17+x] = R
        m[18+x] = R
        m[27+x] = R
    if n == 5:
        m[1+x] = R
        m[2+x] = R
        m[9+x] = R
        m[17+x] = R
        m[18+x] = R
        m[27+x] = R
        m[33+x] = R
        m[34+x] = R
    if n == 6:
        m[1+x] = R
        m[2+x] = R
        m[9+x] = R
        m[17+x] = R
        m[18+x] = R
        m[25+x] = R
        m[27+x] = R
        m[33+x] = R
        m[34+x] = R
    if n == 7:
        m[1+x] = R
        m[2+x] = R
        m[11+x] = R
        m[27+x] = R
    if n == 8:
        m[1+x] = R
        m[2+x] = R
        m[9+x] = R
        m[11+x] = R
        m[17+x] = R
        m[18+x] = R
        m[25+x] = R
        m[27+x] = R
        m[33+x] = R
        m[34+x] = R  
    if n == 9:
        m[1+x] = R
        m[2+x] = R
        m[9+x] = R
        m[11+x] = R
        m[17+x] = R
        m[18+x] = R
        m[27+x] = R
        m[33+x] = R
        m[34+x] = R
    if n == 0:
        m[1+x] = R
        m[2+x] = R
        m[9+x] = R
        m[11+x] = R
        m[17+x] = R
        m[25+x] = R
        m[27+x] = R
        m[33+x] = R
        m[34+x] = R
        
    return m