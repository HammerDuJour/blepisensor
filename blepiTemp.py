import pexpect
import sys
import time
import datetime
import sqlite3

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
    
    cursor.execute("INSERT INTO log(tagDate,logDate,temp,ambTemp,tagAddr,ipAddr) VALUES(%,%,%,%,%,%), 1, 1, temp,ambTemp,tagAddr,ipAddr")
    
    connection.commit()
    connection.close()

def connect(tool):
    print "Connecting to Sensor Tag"
    tool.sendline('connect')
    index = tool.expect (['Connection successful', pexpect.TIMEOUT, pexpect.EOF],3)
    if index == 0:
    	tool.sendline('char-write-cmd 0x29 01')
    	tool.expect('\[LE\]>')
    else:
	tool = None

def bleTempCollection(interval=1):

    print "Create Tools Variable"
    tools = []
    SensorTags = []
    
    stConn = sqlite3.connect('/home/pi/blepisensor/SensorInfo.db')
    stCursor = stConn.cursor()
	
	# Read Sensor Tag addresses from a local database
    for row in stCursor.execute("SELECT * FROM SensorTags"):
	print row[1]
	print row[2]
	lf = open(logfile, 'a')
	tool = pexpect.spawn('gatttool -b ' + row[1] + ' --interactive',logfile=lf)
		
	tool.expect('\[LE\]>')
	connect(tool)
		
	st = SensorTag(row[1],tool,row[2])
	SensorTags.append(st)
	
    stConn.close()
	
    # create a collection of pexpect tools
#    for address in addresses:
#       if logfile != '': 
#            print "Create tool with log file"
#            lf = open(logfile, 'a')
#            tool = pexpect.spawn('gatttool -b ' + address + ' --interactive',logfile=lf)
#        else:
#            print "Create tool, No log file"
#            tool = pexpect.spawn('gatttool -b ' + address + ' --interactive')        
#            
#        tool.expect('\[LE\]>')
#        connect(tool)
#        tools.append(tool) # why am I appending to a collection of tools??
#        st = SensorTag(address,tool,descriptions[i])
#        i = i + 1
#        SensorTags.append(st)
  
    #iterate over each tool in tools and retrieve temp data
    while True:
        for sensorTag in SensorTags:
            
            tool = sensorTag.control
            if tool is None:
  		print "Tool is None"
            else:
		tool.sendline('char-read-hnd 0x25')
		index = tool.expect (['descriptor: .*', 'Disconnected', pexpect.EOF, pexpect.TIMEOUT],3)
                if index == 0:
                    hexStr = tool.after
                    ambient = ambientTemp(hexStr)
                    irT = irTemp(hexStr)
                    saveData(["ambientTemp", ambient, "IR Temp", irT])
  	    	    saveDataToDB(irT,ambient,sensorTag.mac,0)
                elif index == 1:
                    connect(tool)
                
        time.sleep(float(interval))
                
    # will this crash if lf is not created ?
    lf.close()        
    
#TODO: cleanup usage and catch erroneous input in main
#TODO: Create a DEbug() function and flag next time I need to debug

def main():
    if (len(sys.argv) < 2):
        # get mac addresses from file
        #addresses = ['BC:6A:29:AB:D5:92','BC:6A:29:AB:23:DA','BC:6A:29:AB:3B:4B', 'BC:6A:29:AB:23:F6']
        #descriptions = ['Tag 1','Tag 2','Tag 3','Tag 4']        
        bleTempCollection()
    elif (len(sys.argv) == 2):
        bleTemp(sys.argv[1])
    else:
        bleTemp(sys.argv[1],sys.argv[2])

if __name__ == '__main__':
    main()
