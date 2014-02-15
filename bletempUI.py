import time 
from Tkinter import *
from random import randint

class MyApp:
    def __init__(self,parent):
        
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
        self.getMeasurements()
    

    def getMeasurements(self):
        while True:
            vals = measure()
            self.DataAmbient0["text"] = vals[0]
            self.DataIR0["text"] = vals[1]

            vals = measure()
            self.DataAmbient1["text"] = vals[0]
            self.DataIR1["text"] = vals[1]
            
            time.sleep(1)
            root.update()
                    
       
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
        
       
root = Tk()
myapp = MyApp(root)
root.mainloop()
        
