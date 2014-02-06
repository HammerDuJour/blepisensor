#!/usr/bin/env python

import pexpect
import sys
import time
import datetime
from SensorTag import *
from SensorCalcs import *

csvfile = r'testfile.csv'
#set this empty to turn off logging:
logfile = r'pexpect.log'

def usage():
    print 'blepisensor.py Usage:'
    print '  blepisensor.py address [interval]'
    print ''
    print '  address    The address of the sensor to read.'
    print '  interval   The reading interval in seconds.  Default is 1.'

#def floatfromhex(h):
#    t = float.fromhex(h)
#    if t > float.fromhex('7FFF'):
#        t = -(float.fromhex('FFFF') - t)
#        pass
#    return t

#def calcTmpTarget(objT, ambT):
#    m_tmpAmb = ambT/128.0
#    Vobj2 = objT * 0.00000015625
#    Tdie2 = m_tmpAmb + 273.15
#    S0 = 6.4E-14
#    a1 = 1.75E-3
#    a2 = -1.678E-5
#    b0 = -2.94E-5
#    b1 = -5.7E-7
#    b2 = 4.63E-9
#    c2 = 13.4
#    Tref = 298.15
#    S = S0*(1+a1*(Tdie2 - Tref)+a2*pow((Tdie2 - Tref),2))
#    Vos = b0 + b1*(Tdie2 - Tref) + b2*pow((Tdie2 - Tref),2)
#    fObj = (Vobj2 - Vos) + c2*pow((Vobj2 - Vos),2)
#    tObj = pow(pow(Tdie2,4) + (fObj/S),.25)
#    tObj = (tObj - 273.15)
    
#    print(round(tObj,2))
#    return tObj
    
def saveData(hexStr):
    #print "after expect"
    rval = hexStr.split()
    #print "printing rval"
    objT = floatfromhex(rval[2] + rval[1])
    ambT = floatfromhex(rval[4] + rval[3])
    #print rval
    temp = calcTmpTarget(objT,ambT)
    timestamp = datetime.datetime.now().strftime("%y-%m-%d-%H:%M:%S")
    #print timestamp
    
    f = open(csvfile,"a")
    f.write("\"" + timestamp + "\",\"" + str(temp) + "\",\"" + str(ambT) + "\"\n")
    f.close()

def connect(tool):
    print "Inside Connect: Sendline Connect"
    tool.sendline('connect')
    print "test for success of connect"
    tool.expect('Connection successful')   
    print "turn on temperature sensor"
    tool.sendline('char-write-cmd 0x29 01')
    tool.expect('\[LE\]>')

#class SensorTag:
#    def __init__(self,mac,control):
#        self.mac = mac
#        self.control = control

def bleTempCollection(addresses, interval=1):

    print "Create Tools Variable"
    tools = []
    SensorTags = []
    
    # create a collection of pexpect tools
    for address in addresses:
        print "address"
        print address
        if logfile != '': 
            print "Create tool with log file"
            lf = open(logfile, 'a')
            tool = pexpect.spawn('gatttool -b ' + address + ' --interactive',logfile=lf)
        else:
            print "Create tool, No log file"
            tool = pexpect.spawn('gatttool -b ' + address + ' --interactive')        
            
        tool.expect('\[LE\]>')
        print "After Expect"
        connect(tool)
        print "After Connect"
        tools.append(tool)
        print "tool added to tools"
        st = SensorTag(address,tool)
        SensorTags.append(st)
  
    #iterate over each tool in tools and retrieve temp data
    while True:
        #print "Enter while loop"
        for sensorTag in SensorTags:
            tool = sensorTag.control
            #print "entering for loop. Sendline"
            print(sensorTag.mac)
            tool.sendline('char-read-hnd 0x25')
            #print "sleep"
            time.sleep(float(interval))
            #print "getting index"
            index = tool.expect (['descriptor: .*', 'Disconnected', pexpect.EOF, pexpect.TIMEOUT],3)
            #print "index"
            #print index
            if index == 0:
                saveData(tool.after)
            elif index == 1:
                connect(tool)
                
    # will this crash if lf is not created ?
    lf.close()        
    
#TODO: cleanup usage and catch erroneous input in main
    
def main():
    if (len(sys.argv) < 2):
        # get mac addresses from file
        macs = ['BC:6A:29:AB:D5:92','BC:6A:29:AB:23:DA']
        bleTempCollection(macs)
    elif (len(sys.argv) == 2):
        bleTemp(sys.argv[1])
    else:
        bleTemp(sys.argv[1],sys.argv[2])

if __name__ == '__main__':
    main()
