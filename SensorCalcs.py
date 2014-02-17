def floatfromhex(h):
    t = float.fromhex(h)
    if t > float.fromhex('7FFF'):
        t = -(float.fromhex('FFFF') - t)
        pass
    return t

def calcTmpTarget(objT, ambT):
    m_tmpAmb = ambT/128.0
    Vobj2 = objT * 0.00000015625
    Tdie2 = m_tmpAmb + 273.15
    S0 = 6.4E-14
    a1 = 1.75E-3
    a2 = -1.678E-5
    b0 = -2.94E-5
    b1 = -5.7E-7
    b2 = 4.63E-9
    c2 = 13.4
    Tref = 298.15
    S = S0*(1+a1*(Tdie2 - Tref)+a2*pow((Tdie2 - Tref),2))
    Vos = b0 + b1*(Tdie2 - Tref) + b2*pow((Tdie2 - Tref),2)
    fObj = (Vobj2 - Vos) + c2*pow((Vobj2 - Vos),2)
    tObj = pow(pow(Tdie2,4) + (fObj/S),.25)
    tObj = (tObj - 273.15)
   
    print(round(tObj,2))
    print(round(m_tmpAmb,2))
    return tObj

def ambientTemp(hexStr):
    rval = hexStr.split()
    ambT = return (floatfromhex(rval[4] + rval[3]) / 128)

def irTemp(hexStr):
    rval = hexStr.split()
    objT = floatfromhex(rval[2] + rval[1])
    ambT = floatfromhex(rval[4] + rval[3])
    temp = calcTmpTarget(objT,ambT)
    return temp

def humidity(hexStr):
    rval = hexStr.split()
    rawT = floatfromhex(rval[2] + rval[1])
    rawH = floatfromhex(rval[4] + rval[3])
    humid = calcHum(rawT, rawH)
    
    return humid[1]

#
# Again from http://processors.wiki.ti.com/index.php/SensorTag_User_Guide#Gatt_Server
#
def calcHum(rawT, rawH):
    # -- calculate temperature [deg C] --
    t = -46.85 + 175.72/65536.0 * rawT

    rawH = float(int(rawH) & ~0x0003); # clear bits [1..0] (status bits)
    # -- calculate relative humidity [%RH] --
    rh = -6.0 + 125.0/65536.0 * rawH # RH= -6 + 125 * SRH/2^16
    return (t, rh)