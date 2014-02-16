
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

  
def saveData(hexStr):
    rval = hexStr.split()
    objT = floatfromhex(rval[2] + rval[1])
    ambT = floatfromhex(rval[4] + rval[3])
    temp = calcTmpTarget(objT,ambT)
    timestamp = datetime.datetime.now().strftime("%y-%m-%d-%H:%M:%S")
    
    f = open(csvfile,"a")
    f.write("\"" + timestamp + "\",\"" + str(temp) + "\",\"" + str(ambT) + "\"\n")
    f.close()
    
    vals = {}
    vals[0] = ambT/128
    vals[1] = temp
    return vals

def getHumidity(hexStr):
    rval = hexStr.split()
    rawT = floatfromhex(rval[2] + rval[1])
    rawH = floatfromhex(rval[4] + rval[3])
    humid = calcHum(rawT, rawH)
    
    print "Humidity"
    print humid[1]
    return humid[1]

def connect(tool):
    print "Connecting to Sensor Tag"
    tool.sendline('connect')
    tool.expect('Connection successful')   
    tool.sendline('char-write-cmd 0x29 01')
    tool.expect('\[LE\]>')

    if (measureHumid):
        tool.sendline('char-write-cmd 0x3C 01')
        tool.expect('\[LE\]>')

def report_event(event):
    event_name = {"2": "KeyPress", "4": "ButtonPress"}
    print "Time:", str(event.time)   ### (6)
    print "EventType=" + str(event.type), \
        event_name[str(event.type)],\
        "EventWidgetId=" + str(event.widget), \
        "EventKeySymbol=" + str(event.keysym)      
        
# UI Code
class MyApp:
    def __init__(self, parent, addresses, descriptions, interval):
        
        self.myParent = parent
        
        self.myContainerDisplay = Frame(parent)
        self.myContainerDisplay.pack()
        
        # Holds the HEadings
        self.myContainer1 = Frame(self.myContainerDisplay)
        self.myContainer1.pack()

        # First row of data
        self.myContainer2 = Frame(self.myContainerDisplay)
        self.myContainer2.pack()

        self.myContainer3 = Frame(self.myContainerDisplay)
        #self.myContainer3.pack()

        self.myContainerN = Frame(self.myContainerDisplay)
        self.myContainerN.pack()
        
        self.createWidgets(len(addresses))
        self.getMeasurements(addresses, descriptions, interval)
    

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
                #self.DataAddress0["text"] = sensorTag.description
                self.AddressInfos[sindex]["text"] = sensorTag.description
                
                time.sleep(float(interval))
                tool.sendline('char-read-hnd 0x25')
                index = tool.expect (['descriptor: .*', 'Disconnected', pexpect.EOF, pexpect.TIMEOUT],3)
                
                if index == 0:
                    temps = saveData(tool.after)
                elif index == 1:
                    connect(tool)
                    
                f = temps[0] * 9 / 5
                f = f + 32    
                #self.DataAmbient0["text"] = str(round(f,2)) + " f"
                #self.DataIR0["text"] = str(round(temps[1],2))
                self.TempInfos[sindex]["text"] = str(round(f,2)) + " f"
                self.HumidInfos[sindex]["text"] = str(round(temps[1],2))
                
                # TODO: This meathod needs some cleanup. 
                # The save and measure code is all wrapped together
                if measureHumid:
                    tool.sendline('char-read-hnd 0x38')
                    index = tool.expect (['descriptor: .*', 'Disconnected', pexpect.EOF, pexpect.TIMEOUT],3)
                    
                    if index == 0:
                        humid = getHumidity(tool.after)
                        #self.DataIR0["text"] = str(round(humid,2)) + " %RH"
                        self.HumidInfos[sindex]["text"] = str(round(humid,2)) + " %RH"

            
                root.update()
                sindex = sindex + 1
            
        lf.close()
                    
       
    def createWidgets(self, listLen):
        
        fontSettings=('Verdana', 18, 'bold')
        widgetWidth = "20"
        padding = "0"
        
        # Labels
        self.LabelAddress = Label(self.myContainer1, text="Address", width=widgetWidth, font=fontSettings)
        self.LabelAmbient = Label(self.myContainer1, text="Ambient Temp", width=widgetWidth, padx = padding,font=fontSettings)
        self.LabelIR = Label(self.myContainer1, text="IR Temp", width=widgetWidth, padx = padding, font=fontSettings)
        
        if measureHumid:
            self.LabelIR["text"] = "Humidity"

        self.LabelAddress.pack(side=LEFT)
        self.LabelAmbient.pack(side=LEFT)
        self.LabelIR.pack(side=LEFT)
        
        
        self.AddressInfos = []
        self.TempInfos = []
        self.HumidInfos = []
        
        for index in range(listLen):
            self.AddressInfos[index] = Label(self.myContainer2, text="val", width=widgetWidth, padx = padding, font=fontSettings)
            self.TempInfos[index] = Label(self.myContainer2, text="val", width=widgetWidth, padx = padding, font=fontSettings)
            self.HumidInfos[index] = Label(self.myContainer2, text="val", width=widgetWidth, padx = padding, font=fontSettings)
            
            self.AddressInfos[index].pack()
            self.TempInfos[index].pack()
            self.HumidInfos[index].pack()

        # Data Values
        #self.DataAddress0 = Label(self.myContainer2, text="val", width=widgetWidth, padx = padding, font=fontSettings)
        #self.DataAmbient0 = Label(self.myContainer2, text="val", width=widgetWidth, padx = padding, font=fontSettings)
        #self.DataIR0 = Label(self.myContainer2, text="val", width=widgetWidth, padx = padding, font=fontSettings)

        #self.DataAddress1 = Label(self.myContainer3, text="val", width=widgetWidth, padx = padding, font=fontSettings)
        #self.DataAmbient1 = Label(self.myContainer3, text="val", width=widgetWidth, padx = padding, font=fontSettings)
        #self.DataIR1 = Label(self.myContainer3, text="val", width=widgetWidth, padx = padding, font=fontSettings)
        
        #self.DataAddress0.pack(side=LEFT)
        #self.DataAmbient0.pack(side=LEFT)
        #self.DataIR0.pack(side=LEFT)

        #self.DataAddress1.pack(side=LEFT)
        #self.DataAmbient1.pack(side=LEFT)
        #self.DataIR1.pack(side=LEFT)
        
        # Buttons
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
descriptions = ['Tag 1','Tag 2']
       
root = Tk()
myapp = MyApp(root, addresses, descriptions, 2)
root.mainloop()
        
