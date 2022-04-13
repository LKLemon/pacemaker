import serial
from tkinter import messagebox
from serial.tools import list_ports
from tkinter import *
import math
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as animation
from struct import *

Font_tuple = ("Times", 17, "bold")
Font_tuple2 = ("Times", 15, "bold")


"""
Module: Serial Communication
Description: Serial commnuication between the DCM and Pacemaker. Allow the user to pass the set data to the pacemaker and read data out from the Pacemaker
"""

'''*** ready-to-be-used data. Construct the stored data with corresponding user into list for further usage '''
def inputPass(name,mode):
    global myListGet,pacing_mode
    pacing_mode = mode
    rows = 0
    k = 0
    myList = []
    myListGet = []
    file = open("parameters.txt", "r")
    lines = file.readlines()
    for i in lines:
        Name = i.strip("\n")
        myList.append(Name + '\n')
        k += 1
        if (Name == name):
            rows = k
    for j in range(rows-1,rows+10):
        splitted = myList[j].strip("\n")
        splittedTwice = splitted.split("\t")
        myListGet.append(splittedTwice)
    print(myListGet)
    serialC()

'''***Start the serial communication, pack and unpack the data'''
def serialC():
    try:
        ser = serial.Serial(port="COM", baudrate=115200)
    except:
        return messagebox.showerror("System Message", "Unable to pass")

    SYNC = str.encode("\x16")
    WRITE = str.encode("\x55")
    READEGRAM = str.encode("\x47")
    READPARAM = str.encode("\x22")

    '''@@@Preset the data@@@'''
    'Data for AOO'
    PACING_MODE = 0
    ATR_AMPLITUDE = 70
    VENT_AMPLITUDE = 0
    ATR_WIDTH = 10
    VENT_WIDTH = 0
    AV_Delay = 0
    ARP = 0
    VRP = 0
    Threshold = 10
    LRL = 60
    URL = 120
    ReactionTime = 0
    ResponseFactor = 0
    RecoverTime = 0
    MaxSensorRate = 0
    ATR_Sensitivity = 3
    VENT_Sensitivity = 3

    #Echo egram
    egramdataStr = "\x16"+"\x47" + "\x01" * 17
    egramdataByte = str.encode(egramdataStr)
    #ser.write(egramdataByte)
    #egramdata = ser.read(16)
    #print("egramdata")
    #print(egramdata)

    #SEND PARAMS
    paramStr = "\x16"+"\x22" + "\x01" * 17
    paramByte = str.encode(paramStr)
    # ser.write(paramByte)
    # paramByte = ser.read(16)
    # print("paramByte")
    # print(paramByte)

    myVarList = ["AOO", "VOO", "AAI", "VVI", "DOO", "AOOR", "VOOR", "AAIR", "VVIR", "DOOR"]
    myVarCode = ["\x00", "\x01", "\x02", "\x03", "\x04", "\x05", "\x06", "\x07", "\x08", "\x09"]
    mode = 0

    '''@@@ determine the mode that selected to pass data @@@'''
    for i in range(1, len(myListGet)):      #loop through 10 lines2
        print("myListGet[i][0]")
        print(myListGet[i][0])
        if myVarList[i-1] == pacing_mode:
            mode = i
            print("mode")
            print(mode)
            break
    print(myListGet)
    '''@@@ set ready-to-be-used data to the corresponding variables @@@'''
    LRL = myListGet[mode][1]
    URL = (myListGet[mode][2])
    if mode == 1:
        PACING_MODE = str.encode("\x00")
        print(1)
        ATR_AMPLITUDE = (myListGet[mode][3])
        ATR_WIDTH = (myListGet[mode][4])
    elif mode == 2:
        print("x01")
        PACING_MODE = str.encode("\x01")
        VENT_AMPLITUDE = (myListGet[mode][3])
        print(VENT_AMPLITUDE)
        VENT_WIDTH = (myListGet[mode][4])
        print(VENT_WIDTH)
    elif mode == 3:
        print(2)
        PACING_MODE = str.encode("\x02")
        ATR_AMPLITUDE = (myListGet[mode][3])
        ATR_WIDTH = (myListGet[mode][4])
        print(ATR_WIDTH)
        ATR_Sensitivity= myListGet[mode][5]
        print(ATR_Sensitivity)
        ARP = (myListGet[mode][6])
    elif mode == 4:
        PACING_MODE = str.encode("\x03")
        VENT_AMPLITUDE = (myListGet[mode][3])
        VENT_WIDTH = (myListGet[mode][4])
        VENT_Sensitivity= (myListGet[mode][5])
        VRP = (myListGet[mode][6])
    elif mode == 5:
        PACING_MODE = str.encode("\x04")
        AV_Delay = (myListGet[mode][3])
        ATR_AMPLITUDE = (myListGet[mode][4])
        VENT_AMPLITUDE = (myListGet[mode][5])
        ATR_WIDTH = (myListGet[mode][6])
        VENT_WIDTH = (myListGet[mode][7])
    elif mode == 6:
        PACING_MODE = str.encode("\x05")
        MaxSensorRate = (myListGet[mode][3])
        ATR_AMPLITUDE = (myListGet[mode][4])
        ATR_WIDTH = (myListGet[mode][5])
        Threshold = myListGet[mode][6]
        ReactionTime = (myListGet[mode][7])
        ResponseFactor = (myListGet[mode][8])
        RecoverTime = (myListGet[mode][9])
    elif mode == 7:
        PACING_MODE = str.encode("\x06")
        MaxSensorRate = (myListGet[mode][3])
        ATR_AMPLITUDE = (myListGet[mode][4])
        ATR_WIDTH = (myListGet[mode][5])
        ATR_Sensitivity =myListGet[mode][6]
        ARP = (myListGet[mode][7])
        Threshold = myListGet[mode][11]
        ReactionTime = (myListGet[mode][12])
        ResponseFactor = (myListGet[mode][13])
        RecoverTime = (myListGet[mode][14])
    elif mode == 8:
        PACING_MODE = str.encode("\x07")
        MaxSensorRate = (myListGet[mode][3])
        ATR_AMPLITUDE = (myListGet[mode][4])
        VENT_WIDTH = (myListGet[mode][5])
        Threshold = myListGet[mode][6]
        ReactionTime = (myListGet[mode][7])
        ResponseFactor = (myListGet[mode][8])
        RecoverTime = (myListGet[mode][9])
    elif mode == 9:
        PACING_MODE = str.encode("\x08")
        MaxSensorRate = (myListGet[mode][3])
        ATR_AMPLITUDE = (myListGet[mode][4])
        VENT_WIDTH = (myListGet[mode][5])
        VENT_Sensitivity = (myListGet[mode][6])
        VRP = (myListGet[mode][7])
        Threshold = myListGet[mode][10]
        ReactionTime = (myListGet[mode][11])
        ResponseFactor = (myListGet[mode][12])
        RecoverTime = (myListGet[mode][13])
    elif mode == 10:
        PACING_MODE = str.encode("\x09")
        MaxSensorRate = (myListGet[mode][3])
        AV_Delay = (myListGet[mode][4])
        ATR_AMPLITUDE = (myListGet[mode][5])
        VENT_AMPLITUDE = (myListGet[mode][6])
        ATR_WIDTH = (myListGet[mode][7])
        VENT_WIDTH = (myListGet[mode][8])
        Threshold = myListGet[mode][9]
        ReactionTime = (myListGet[mode][10])
        ResponseFactor = (myListGet[mode][11])
        RecoverTime = (myListGet[mode][12])
    if (ATR_AMPLITUDE == 'OFF'):
        ATR_AMPLITUDE = 0
    if (VENT_AMPLITUDE == 'OFF'):
        VENT_AMPLITUDE = 0
    dutyCycleA = int(ATR_AMPLITUDE)/50
    dutyCycleV = int(VENT_AMPLITUDE) / 50
    dutyCycleAS = int(ATR_Sensitivity) / 50
    dutyCycleVS = int(VENT_Sensitivity) / 50
    if(Threshold == 'V-Low'):Threshold = 33
    if (Threshold == 'Low'): Threshold = 40
    if (Threshold == 'Med-Low'): Threshold =45
    if (Threshold == 'Med'): Threshold = 50
    if (Threshold == 'Med-High'): Threshold =60
    if (Threshold == 'High'): Threshold =70
    if (Threshold == 'V-High'): Threshold = 80
    intArray = [int(dutyCycleA), int(dutyCycleV), int(ATR_WIDTH), int(VENT_WIDTH), int(AV_Delay),int(ARP), int(VRP), Threshold, int(LRL),int(URL), int(ReactionTime), int(ResponseFactor), int(RecoverTime), int(MaxSensorRate),int(dutyCycleAS), int(dutyCycleVS)]

    intByte = b''
    for i in intArray:
        intByte = intByte + i.to_bytes(1,'little')

    cmdByte = SYNC + WRITE + PACING_MODE + intByte
    ser.write(cmdByte)
    print("cmdByte")
    print(cmdByte,len(cmdByte))

    ser.close()

    print("inData4")


    messagebox.showinfo("System Message", "Successully passed")


'''*********************Display Egram********************'''
def showegram(Username):
    Graph = Toplevel()
    Graph.wm_title("egram")
    Graph.geometry("700x500")
    fig = Figure(figsize=(7,4), dpi=100)
    #fig2 = Figure(figsize=(7, 4), dpi=100)

    a = fig.add_subplot(111)
    #b = fig2.add_subplot(111)
    a.grid(True )
    #b.grid(column= 0,row = 2 )
    a.set_title("Electrogram A: " + Username)
    #b.set_title("Electrogram V: " + Username)
    a.set_xlabel("Time")
    a.set_ylabel("Amplitude")


    ecanvas = FigureCanvasTkAgg(fig, Graph)
    ecanvas.draw()
    #ecanvas2 = FigureCanvasTkAgg(fig2, Graph)
    #ecanvas2.draw()

    # toolbars at bottom
    ecanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(ecanvas, Graph)
    toolbar.update()
    ecanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    global tVal,aVal,vVal
    global tList,aList,vList
    tVal,aVal,vVal = 0,0,0
    tList,aList,vList = [],[],[]
    timeInt = .5

    def _quit():
        Graph.quit()     # stops mainloop
        Graph.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    def animate(i):
        global tVal,aVal,vVal
        global tList,aList,vList

        tVal += timeInt       # x is going up in time
        aVal = math.sin(tVal)*1000 # a = atrial, v = ventricular
        vVal = math.cos(tVal)*1000 # HAVE TO BUMP IT UP BC IT WONT PLOT SMALL VALUES, CAN CHANGE AXIS LATER

                                    # change to input values recieved from pacemaker
        tList.append(tVal)              # append to list to graph and write to datafile

        try:
            ser = serial.Serial('COM6', baudrate=115200)
            ser.timeout =5
        except:
            messagebox.showinfo("Pacemaker Connection Error", "The pacemaker is not connected!")
            return

        cmd = b'\x16\x47'+b'\x00'*17
        ser.write(cmd)
        sent_info = ser.read(16)
        print(sent_info )
        info = list(unpack('dd',sent_info))
        ser.close()

        aList.append(info[0]*3.3)
        vList.append(info[1]*3.3)

        a.clear()
        Li = a.plot(tList[-10:],aList[-10:],tList[-10:],vList[-10:])  # plots last 10 points
        a.set_ylim([-3.3,3.3])
        a.set_xlabel("Time")
        a.set_ylabel("Ampltiude")
        a.set_title("Electrogram Data for " + Username)
        return Li             # blit requires you to return your plot to save resources by not redrawing the whole thing

    button = Button(Graph, text="Quit", command=_quit)
    button.pack(side=BOTTOM)

    ani = animation.FuncAnimation(fig,animate,interval=timeInt*100,blit=True)
    mainloop()

