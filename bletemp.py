import pexpect
import sys
import time
import datetime

csvfile = r'testfile.csv'
#set this empty to turn off logging:
logfile = r'pexpect.log'

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
    
    print tObj
    return tObj
    
def saveData(hexStr):
    #print "after expect"
    rval = hexStr.split()
    #print "printing rval"
    objT = floatfromhex(rval[2] + rval[1])
    ambT = floatfromhex(rval[4] + rval[3])
    #print rval
    temp = calcTmpTarget(objT,ambT)
    timestamp = datetime.datetime.now().strftime("%y-%m-%d-%H:%M:%S")
    print timestamp
    
    f = open(csvfile,"a")
    f.write("\"" + timestamp + "\",\"" + str(temp) + "\",\"" + str(ambT) + "\"\n")
    f.close()

def connect(tool):
    tool.sendline('connect')
    #print "test for success of connect"
    tool.expect('Connection successful')   
    #print "turn on temperature sensor"
    tool.sendline('char-write-cmd 0x29 01')
    tool.expect('\[LE\]>')

    
def bleTemp(bluetooth_adr, interval=1):

    if logfile != '': 
        lf = open(logfile, 'a')
        tool = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive',logfile=lf)
    else:
        tool = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive')
    
    tool.expect('\[LE\]>')
    #print "Preparing to connect. You might need to press the side button"
    #print "send connect"
    connect(tool)
    
    while True:
        time.sleep(1)
        #print "poll for temperature"
        tool.sendline('char-read-hnd 0x25')
        #print "expect descriptor"

	index = tool.expect (['descriptor: .*', 'Disconnected', pexpect.EOF, pexpect.TIMEOUT],3)
        if index == 0:
            saveData(tool.after)
        elif index == 1:
            connect(tool)
        #elif index == 2 or index == 3:
            #print 'pexpect died, eof or timeout'
            #exit()

    lf.close()    
    
        
def main():
    if (len(sys.argv) == 2):
        bleTemp(sys.argv[1])
    else:
        bleTemp(sys.argv[1],sys.argv[2])

if __name__ == '__main__':
    main()
