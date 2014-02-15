
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


def usage():
    print 'blepisensor.py Usage:'
    print '  blepisensor.py address [interval]'
    print ''
    print '  address    The address of the sensor to read.'
    print '  interval   The reading interval in seconds.  Default is 1.'

  
def saveData(hexStr):
    rval = hexStr.split()
    objT = floatfromhex(rval[2] + rval[1])
    ambT = floatfromhex(rval[4] + rval[3])
    temp = calcTmpTarget(objT,ambT)
    timestamp = datetime.datetime.now().strftime("%y-%m-%d-%H:%M:%S")
    
    f = open(csvfile,"a")
    f.write("\"" + timestamp + "\",\"" + str(temp) + "\",\"" + str(ambT) + "\"\n")
    f.close()
    
    return temp

def connect(tool):
    print "Connecting to Sensor Tag"
    tool.sendline('connect')
    tool.expect('Connection successful')   
    tool.sendline('char-write-cmd 0x29 01')
    tool.expect('\[LE\]>')

def report_event(event):
    event_name = {"2": "KeyPress", "4": "ButtonPress"}
    print "Time:", str(event.time)   ### (6)
    print "EventType=" + str(event.type), \
        event_name[str(event.type)],\
        "EventWidgetId=" + str(event.widget), \
        "EventKeySymbol=" + str(event.keysym)      
        
def measure():
    vals = {}
    vals[0] = randint(45,99)
    vals[1] = randint(45,99)
    return vals

# UI Code
class MyApp:
    def __init__(self, parent, addresses, interval):
        
        self.myParent = parent
        self.myContainerConfig = Frame(parent, bg="black")
        self.myContainerConfig.pack(side=LEFT)
        
        self.myContainerDisplay = Frame(parent)
        self.myContainerDisplay.pack()
        
        self.myContainer1 = Frame(self.myContainerDisplay)
        self.myContainer1.pack()

        self.myContainer2 = Frame(self.myContainerDisplay)
        self.myContainer2.pack()

        self.myContainer3 = Frame(self.myContainerDisplay)
        self.myContainer3.pack()

        self.myContainerN = Frame(self.myContainerDisplay)
        self.myContainerN.pack()
        
        self.createWidgets()
        self.getMeasurements(addresses, interval)
    

    def getMeasurements(self, addresses, interval):
               
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
            st = SensorTag(address,tool)
            SensorTags.append(st)
        
        while True:
            
            for sensorTag in SensorTags:
                tool = sensorTag.control
                self.DataAddress0["text"] = sensorTag.mac
                
                tool.sendline('char-read-hnd 0x25')
                time.sleep(float(interval))
                index = tool.expect (['descriptor: .*', 'Disconnected', pexpect.EOF, pexpect.TIMEOUT],3)
                
                if index == 0:
                    temp = saveData(tool.after)
                elif index == 1:
                    connect(tool)
                    
                self.DataIR0["text"] = str(temp)
            
                root.update()
            
        lf.close()
                    
       
    def createWidgets(self):
        
        fontSettings=('Verdana', 18, 'bold')
        widgetWidth = "14"
        padding = "0"
        
        # Config buttons
        self.testButton = Button(self.myContainerConfig, width = "5")
        self.testButton.pack()
        self.testButton = Button(self.myContainerConfig, width = "5")
        self.testButton.pack()
        self.testButton = Button(self.myContainerConfig, width = "5")
        self.testButton.pack()
        self.testButton = Button(self.myContainerConfig, width = "5")
        self.testButton.pack()
                
        # Labels
        self.LabelAddress = Label(self.myContainer1, text="Address", width=widgetWidth, font=fontSettings)
        self.LabelAmbient = Label(self.myContainer1, text="Ambient Temp", width=widgetWidth, padx = padding,font=fontSettings)
        self.LabelIR = Label(self.myContainer1, text="IR Temp", width=widgetWidth, padx = padding, font=fontSettings)

        self.LabelAddress.pack(side=LEFT)
        self.LabelAmbient.pack(side=LEFT)
        self.LabelIR.pack(side=LEFT)

        # Data Values
        self.DataAddress0 = Label(self.myContainer2, text="val", width=widgetWidth, padx = padding, font=fontSettings)
        self.DataAmbient0 = Label(self.myContainer2, text="val", width=widgetWidth, padx = padding, font=fontSettings)
        self.DataIR0 = Label(self.myContainer2, text="val", width=widgetWidth, padx = padding, font=fontSettings)

        self.DataAddress1 = Label(self.myContainer3, text="val", width=widgetWidth, padx = padding, font=fontSettings)
        self.DataAmbient1 = Label(self.myContainer3, text="val", width=widgetWidth, padx = padding, font=fontSettings)
        self.DataIR1 = Label(self.myContainer3, text="val", width=widgetWidth, padx = padding, font=fontSettings)

        
        self.DataAddress0["text"] = "80:80:80:80"
        self.DataAddress1["text"] = "80:80:80:DA"

        self.DataAddress0.pack(side=LEFT)
        self.DataAmbient0.pack(side=LEFT)
        self.DataIR0.pack(side=LEFT)

        self.DataAddress1.pack(side=LEFT)
        self.DataAmbient1.pack(side=LEFT)
        self.DataIR1.pack(side=LEFT)
        
        # Buttons
        self.button1 = Button(self.myContainerN, text= "Measure", bg="Green")
#        self.button1.pack(side=LEFT)
        self.button1.bind("<Button-1>", self.button1Click)
        self.button1.bind("<Return>", self.button1Click)
        
        self.button2 = Button(self.myContainerN, text="Quit", bg="Red")
        self.button2.pack(side=RIGHT)
        self.button2.bind("<Button-1>", self.button2Click)
        self.button2.bind("<Return>", self.button2Click)
        
    def button1Click(self,event):
        report_event(event)
        vals = measure()
        self.DataAmbient0["text"] = vals[0]
        self.DataAddress0["text"] = vals[1]
        self.DataIR0["text"] = vals[2]
                
    def button2Click(self, event):
        report_event(event)
        self.myParent.destroy()
        
    
addresses = ['BC:6A:29:AB:D5:92','BC:6A:29:AB:23:DA']
       
root = Tk()
myapp = MyApp(root, addresses, 2)
root.mainloop()
        
