
import pexpect
import sys
import time
import datetime

from SensorTag import *
from SensorCalcs import *
from Tkinter import *
from random import randint

csvfile = r'testfile.csv'
#set this empty to turn off logging:
logfile = r'pexpect.log'
measureHumid = True

def usage():
    print 'blepisensor.py Usage:'
    print '  blepisensor.py address [interval]'
    print ''
    print '  address    The address of the sensor to read.'
    print '  interval   The reading interval in seconds.  Default is 1.'

  
def saveData(data):
    timestamp = datetime.datetime.now().strftime("%y-%m-%d-%H:%M:%S")
    f = open(csvfile,"a")
    f.write("\"" + timestamp + "\"")
    for dataPoint in data:
        f.write(",\"" + str(dataPoint) + "\"")
    f.write("\n")
    f.close()

def connect(tool):
    print "Connecting to Sensor Tag"
    tool.sendline('connect')
    tool.expect('Connection successful')   
    tool.sendline('char-write-cmd 0x29 01')
    tool.expect('\[LE\]>')

    # humidity
    tool.sendline('char-write-cmd 0x3C 01')
    tool.expect('\[LE\]>')

# UI Code
class MyApp:
    def __init__(self, parent, addresses, descriptions, interval):
        
        self.myParent = parent
        
        self.createWidgets(addresses, descriptions)
        self.getMeasurements(addresses, descriptions, interval)
    
    #This version has no connection requirement.  Basically for UI debugging
    def getMeasurements_(self, addresses, descriptions, interval):
               
        tools = []
        SensorTags = []
        
        # create a collection of pexpect tools
        i = 0;
        for address in addresses:

            st = SensorTag(address,"tool",descriptions[i])
            i = i + 1
            SensorTags.append(st)
        
        testIndex = 0
        while True:
            
            sindex = 0
            for sensorTag in SensorTags:
                
                ambientTemp = 20
                irTemp = 21
                    
                f = ambientTemp * 9 / 5
                f = f + 32    
                
                irTempF = irTemp * 9 / 5
                irTempF = irTempF + 32

                self.ATempDatas[sindex]["text"] = str(round(f,2) + testIndex) + " f"
                self.IRTempDatas[sindex]["text"] = str(round(irTempF,2)+ testIndex) + " f"
                
                humid = 35
                self.HumdDatas[sindex]["text"] = str(round(humid,2)+ testIndex) + " %RH"

                root.update()
                sindex = sindex + 1
                testIndex += 1
                
                saveData(["ambientTemp", ambientTemp, "IR Temp", irTemp, "Humidity", humid])

            time.sleep(float(interval))
            
        lf.close()


    def getMeasurements(self, addresses, descriptions, interval):
               
        tools = []
        SensorTags = []
        
        # create a collection of pexpect tools
        i = 0;
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
        
        while True:
            
            sindex = 0
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
                    
                f = ambient * 9 / 5
                f = f + 32    
                
                irT = ir * 9 / 5
                irT = irT + 32

                self.ATempDatas[sindex]["text"] = str(round(f,2)) + " f"
                self.IRTempDatas[sindex]["text"] = str(round(irT,2)) + " f"
                
                tool.sendline('char-read-hnd 0x38')
                index = tool.expect (['descriptor: .*', 'Disconnected', pexpect.EOF, pexpect.TIMEOUT],3)
                    
                if index == 0:
                    humid = humidity(tool.after)
                    self.HumdDatas[sindex]["text"] = str(round(humid,2)) + " %RH"

                root.update()
                sindex = sindex + 1
                
                saveData(["ambientTemp", ambient, "IR Temp", irT, "Humidity", humid])

            time.sleep(float(interval))
        lf.close()
                    
       
    def createWidgets(self, addresses, descriptions):
        
        TitleFont=('Verdana', 14, 'bold')
        DataFont= ('Verdana', 14)
        widgetWidth = "11"
        padding = "4"
        
        # Labels
        self.AddrLabel = Label(self.myParent, text="Tag",  font=TitleFont)
        self.AmbTLabel = Label(self.myParent, text="Ambient Temp",padx = padding,font=TitleFont)
        self.IR_TLabel = Label(self.myParent, text="IR Temp",padx = padding,font=TitleFont)
        self.HumdLabel = Label(self.myParent, text="Humidity", padx = padding, font=TitleFont)

        self.AddrLabel.grid(row = 0, column = 0)
        self.AmbTLabel.grid(row = 0, column = 1)
        self.IR_TLabel.grid(row = 0, column = 2)
        self.HumdLabel.grid(row = 0, column = 3)
        
        # Initialize lists for Address, Temperature and Humidity Data        
        self.AddrDatas = []
        self.ATempDatas = []
        self.IRTempDatas = []
        self.HumdDatas = []
        
        for index in range(len(addresses)):

            self.AddrDatas.append(Label(self.myParent, width=widgetWidth, font = DataFont, text = descriptions[index]))
            self.ATempDatas.append(Label(self.myParent, width=widgetWidth, font = DataFont))
            self.IRTempDatas.append(Label(self.myParent, width=widgetWidth, font = DataFont))
            self.HumdDatas.append(Label(self.myParent, width=widgetWidth, font = DataFont))
            
            self.AddrDatas[index].grid(row=index+1, column = 0)
            self.ATempDatas[index].grid(row=index+1, column = 1)
            self.IRTempDatas[index].grid(row=index+1, column = 2)
            self.HumdDatas[index].grid(row=index+1, column = 3)
        
        # Buttons
        self.QuitButton = Button(self.myParent, text="Quit", bg="Red")
        self.QuitButton.grid(columnspan = 4, sticky = E)
        
        self.QuitButton.bind("<Button-1>", self.QuitButtonClick)
        self.QuitButton.bind("<Return>", self.QuitButtonClick)
                
    def QuitButtonClick(self, event):
        self.myParent.destroy()
        
    
addresses = ['BC:6A:29:AB:D5:92','BC:6A:29:AB:23:DA']
descriptions = ['Tag 1','Tag 2']
       
root = Tk()
myapp = MyApp(root, addresses, descriptions, 2)
root.mainloop()
        
