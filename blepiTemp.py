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
    print 'blepiTemp.py Usage:'
    print '  blepiTemp.py'
    print ''
    print '  SensorTag addresses and labels are hardcoded into blepiTemp.py'
  
def saveData(data):
    timestamp = datetime.datetime.now().strftime("%y-%m-%d-%H:%M:%S")
    f = open(csvfile,"a")
    f.write("\"" + timestamp + "\"")
    for dataPoint in data:
        f.write(",\"" + str(dataPoint) + "\"")
    f.write("\n")
    f.close()

def saveDataToDB(temp,ambTemp,tagAddr,ipAddr):
    connection = sqlite3.connect('/home/pi/blepimesh/data/client.db')
    cursor = connection.cursor()
    
	cursor.execute("INSERT INTO log(tagDate,logDate,temp,ambTemp,tagAddr,ipAddr)VALUES(?,?,?,?,?,?)",
	date('now'),time('now'), temp,ambTemp,tagAddr,ipAddr)
    
    connection.commit()
    connection.close()

def connect(tool):
    print "Connecting to Sensor Tag"
    tool.sendline('connect')
    tool.expect('Connection successful')   
    tool.sendline('char-write-cmd 0x29 01')
    tool.expect('\[LE\]>')

def bleTempCollection(addresses, descriptions, interval=1):

    print "Create Tools Variable"
    tools = []
    SensorTags = []
    
    # create a collection of pexpect tools
    for address in addresses:
        if logfile != '': 
            print "Create tool with log file"
            lf = open(logfile, 'a')
            tool = pexpect.spawn('gatttool -b ' + address + ' --interactive',logfile=lf)
        else:
            print "Create tool, No log file"
            tool = pexpect.spawn('gatttool -b ' + address + ' --interactive')        
            
        tool.expect('\[LE\]>')
        connect(tool)
        tools.append(tool)
        st = SensorTag(address,tool,descriptions[i])
        i = i + 1
        SensorTags.append(st)
  
    #iterate over each tool in tools and retrieve temp data
    while True:
        for sensorTag in SensorTags:
            
            tool = sensorTag.control
            tool.sendline('char-read-hnd 0x25')
            index = tool.expect (['descriptor: .*', 'Disconnected', pexpect.EOF, pexpect.TIMEOUT],3)
            if index == 0:
                hexStr = tool.after
                ambient = ambientTemp(hexStr)
                ir = irTemp(hexStr)
            elif index == 1:
                connect(tool)
                
            saveData(["ambientTemp", ambient, "IR Temp", irT])
			saveDataToDB(irT,ambient,sensorTag.mac,0)
			
        time.sleep(float(interval))
                
    # will this crash if lf is not created ?
    lf.close()        
    
#TODO: cleanup usage and catch erroneous input in main
#TODO: Create a DEbug() function and flag next time I need to debug

def main():
    if (len(sys.argv) < 2):
        # get mac addresses from file
        addresses = ['BC:6A:29:AB:D5:92','BC:6A:29:AB:23:DA','BC:6A:29:AB:3B:4B', 'BC:6A:29:AB:23:F6']
        descriptions = ['Tag 1','Tag 2','Tag 3','Tag 4']        
        bleTempCollection(addresses,descriptions,sys.argv[1])
    elif (len(sys.argv) == 2):
        bleTemp(sys.argv[1])
    else:
        bleTemp(sys.argv[1],sys.argv[2])

if __name__ == '__main__':
    main()
