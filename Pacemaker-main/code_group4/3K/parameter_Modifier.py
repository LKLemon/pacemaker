import tkinter as tk
import numpy as np
from Error_msg import *
from serial import *
from serialC import *

Font_tuple2 = ("Times", 15, "bold")

"""
Module: Pacemaker functions
Description: Basic pacemaker functions that allow user to set different modes and diplay the egram and user stored data
"""

'''***Dispaly current stored user data***'''
def verify(name):
    window_ver = tk.Toplevel()
    window_ver.title('Display')
    window_ver.geometry("700x500")

    rows=0
    k=0
    myList = []
    file = open("parameters.txt", "r")
    lines = file.readlines()
    for i in lines:
        Name = i.strip("\n")
        myList.append(Name + '\n')
        k+=1
        if (Name == name): rows = k                                         #Locate the user position in the text file
    st1 = tk.Label(window_ver, text='Current Stored Paramters:')
    st1.grid(column=0,row=0, sticky = 'W')
    lowerL = rows-1
    st2 = tk.Label(window_ver, text=myList[lowerL])                        #Display the list in a proper format
    st3 = tk.Label(window_ver, text=myList[lowerL + 1])
    st4 = tk.Label(window_ver, text=myList[lowerL + 2])
    st5 = tk.Label(window_ver, text=myList[lowerL + 3])
    st6 = tk.Label(window_ver, text=myList[lowerL + 4])
    st7 = tk.Label(window_ver, text=myList[lowerL + 5])
    st8 = tk.Label(window_ver, text=myList[lowerL + 6])
    st9 = tk.Label(window_ver, text=myList[lowerL + 7])
    st10 = tk.Label(window_ver, text=myList[lowerL + 8])
    st11 = tk.Label(window_ver, text=myList[lowerL + 9])
    bt = tk.Button(window_ver, text='Back', command=window_ver.destroy)
    st2.grid(column=0,row=2, sticky = 'W')
    st3.grid(column=0, row=3, sticky = 'W')
    st4.grid(column=0, row=4, sticky = 'W')
    st5.grid(column=0, row=5, sticky = 'W')
    st6.grid(column=0, row=6, sticky = 'W')
    st7.grid(column=0, row=7, sticky = 'W')
    st8.grid(column=0, row=8, sticky = 'W')
    st9.grid(column=0, row=9, sticky = 'W')
    st10.grid(column=0, row=10, sticky = 'W')
    st11.grid(column=0, row=11, sticky = 'W')
    bt.grid(column=0, row=12, sticky = 'W')


'''***Locate user position in parameter.txt***'''
def updateDataGet(name):                                #Intend to pass the user name variable from the main
    global rows
    rows = 0
    print("current user is "+name)
    file = open("parameters.txt", "r")
    lines = file.readlines()
    for i in lines:
        var = i.strip("\n")
        if (var != name):rows += 1
        if (var == name):break
    rows = rows+1
    file.close()
    return rows

'''***AOO mode. Allow user to set, store, and pass data***'''
def parameter_AOO(name):
    window_aoo = tk.Toplevel()
    window_aoo.title('AOO Mode')
    canvas = tk.Canvas(window_aoo,height = 560, width =800)
    canvas.pack()

    tk.Label(window_aoo, text='AOO Mode',font = Font_tuple2).place(x=345, y=45)

    v_lrl = tk.StringVar()
    LRL = tk.Label(window_aoo, text='Lower Rate Limit').place(x=10, y=100)
    tk.Spinbox(window_aoo, state="readonly",
               values=(list(range(30, 50, 5)) + list(range(50, 90, 1)) + list(range(90, 176, 5))), width=8, textvariable=v_lrl).place(x=150, y=100)

    v_url = tk.StringVar()
    tk.Label(window_aoo, text='Upper Rate Limit').place(x=300, y=100)
    tk.Spinbox(window_aoo,state="readonly", values=list(range(50,176,5)), width=8, textvariable=v_url).place(x=450, y=100)

    v_aa = tk.StringVar()
    tk.Label(window_aoo, text='Atrial Amplitude(mV)').place(x=10, y=200)
    tk.Spinbox(window_aoo, state="readonly",values=["OFF"] + list(np.arange(100, 5100, 100)) , width=8,textvariable=v_aa).place(x=150, y=200)

    v_apw = tk.StringVar()
    tk.Label(window_aoo, text='Atrial Pules Width').place(x=300, y=200)
    tk.Spinbox(window_aoo, state="readonly", values=list(np.arange(1, 31, 1)), width=5,
            textvariable=v_apw).place(x=450, y=200)

    '''@@@Fetch the input data@@@'''
    def parameter_AOO_get_info():
        entryed_aa = v_aa.get()
        entryed_apw = v_apw.get()
        entryed_lrl = v_lrl.get()
        entryed_url = v_url.get()
        print("now" )
        print(name, entryed_lrl, entryed_url, entryed_aa, entryed_apw)
        data_update_aoo(name, entryed_lrl, entryed_url, entryed_aa, entryed_apw)

    b1aoo = tk.Button(window_aoo, text='Save',command= parameter_AOO_get_info)
    b2aoo = tk.Button(window_aoo, text='Back', command=window_aoo.destroy)
    b3aoo = tk.Button(window_aoo, text='Stored View', command=lambda:verify(name))
    b4aoo = tk.Button(window_aoo, text='Pass to Pacemaker', command=lambda:inputPass(name,"AOO"))
    b1aoo.place(x=10, y=500)
    b2aoo.place(x=200, y=500)
    b3aoo.place(x=300, y=500)
    b4aoo.place(x=400, y=500)
    b1aoo.pack()
    b2aoo.pack()
    b3aoo.pack()
    b4aoo.pack()


'''***AOO mode update. Write the data into the file***'''
def data_update_aoo(name,v_lrl, v_url, v_aa, v_apw):
    updateDataGet(name)
    print(name,v_lrl, v_url, v_aa, v_apw)
    with open('parameters.txt', 'r') as file:
        data = file.readlines()
        data[rows] = "AOO\t"+v_lrl + '\t'+v_url + '\t'+v_aa + '\t'+v_apw + "\n"         #rewrite a certain line in the file
    with open('parameters.txt', 'w') as file:
        file.writelines(data)                                                              #write the other unchanged line back to the file
    messagebox.showinfo("System Message", "Success!")

'''***VOO mode. Allow user to set, store, and pass data***'''
def parameter_VOO(name):
    windowVoo = tk.Toplevel()
    windowVoo.title('VOO Mode')
    canvas = tk.Canvas(windowVoo,height = 560, width =800)
    canvas.pack()

    tk.Label(windowVoo, text='VOO Mode',font = Font_tuple2).place(x=345, y=45)

    v_lrl = tk.StringVar()
    tk.Label(windowVoo, text='Lower Rate Limit').place(x=10, y=100)
    tk.Spinbox(windowVoo, state="readonly",
               values=(list(range(30, 50, 5)) + list(range(50, 90, 1)) + list(range(90, 176, 5))), width=8,
               textvariable=v_lrl).place(x=150, y=100)

    v_url = tk.StringVar()
    tk.Label(windowVoo, text='Upper Rate Limit').place(x=300, y=100)
    tk.Spinbox(windowVoo, state="readonly", values=list(range(50, 176, 5)), width=8, textvariable=v_url).place(
        x=450, y=100)

    v_va = tk.StringVar()
    tk.Label(windowVoo, text='Ventricular Amplitude(mV)').place(x=10, y=200)
    tk.Spinbox(windowVoo, state="readonly",values=["OFF"] + list(np.arange(100, 5100, 100)) , width=8,
               textvariable=v_va).place(x=150, y=200)

    v_vpw = tk.StringVar()
    tk.Label(windowVoo, text='Ventricular Pulse Width').place(x=300, y=200)
    tk.Spinbox(windowVoo, state="readonly", values=list(np.arange(1, 31, 1)), width=5,
            textvariable=v_vpw).place(x=450, y=200)

    def parameter_VOO_get_info():
        entryed_lrl = v_lrl.get()
        entryed_url = v_url.get()
        entryed_va = v_va.get()
        entryed_vpw = v_vpw.get()
        data_update_voo(name,entryed_lrl, entryed_url, entryed_va, entryed_vpw)

    b1Voo = tk.Button(windowVoo, text='save', command=parameter_VOO_get_info)
    b2Voo = tk.Button(windowVoo, text='back', command=windowVoo.destroy)
    b3Voo = tk.Button(windowVoo, text='Stored View', command=lambda:verify(name))
    b4Voo = tk.Button(windowVoo, text='Pass to Pacemaker', command=lambda: inputPass(name,"VOO"))
    b1Voo.place(x=10, y=500)
    b2Voo.place(x=200, y=500)
    b2Voo.place(x=300, y=500)
    b2Voo.place(x=400, y=500)
    b1Voo.pack()
    b2Voo.pack()
    b3Voo.pack()
    b4Voo.pack()

'''***VOO mode update. Write the data in to the file***'''
def data_update_voo(name,v_lrl, v_url, v_va, v_vpw):
    updateDataGet(name)
    with open('parameters.txt', 'r') as file:  # read a list of lines into data
        data = file.readlines()
        data[rows+1] = "VOO\t" + v_lrl + '\t' + v_url + '\t' + v_va + '\t' + v_vpw + "\n"
    with open('parameters.txt', 'w') as file:
        file.writelines(data)
    messagebox.showinfo("System Message", "Success!")

'''***AAI mode. Allow user to set, store, and pass data***'''
def parameter_AAI(name):
    window = tk.Toplevel()
    window.title('AAI Mode')
    canvas = tk.Canvas(window,height = 560, width =800)
    canvas.pack()

    tk.Label(window, text='AAI Mode',font = Font_tuple2).place(x=345, y=45)

    v_lrl = tk.StringVar()
    tk.Label(window, text='Lower Rate Limit').place(x=10, y=100)
    tk.Spinbox(window, state="readonly",values=(list(range(30, 50, 5)) + list(range(50, 90, 1)) + list(range(90, 176, 5))), width=8,textvariable=v_lrl).place(x=150, y=100)

    v_url = tk.StringVar()
    tk.Label(window, text='Upper Rate Limit').place(x=300, y=100)
    tk.Label(window, text='Upper Rate Limit').place(x=300, y=100)
    tk.Spinbox(window, state="readonly", values=list(range(50, 176, 5)), width=8, textvariable=v_url).place(x=450, y=100)

    v_aa = tk.StringVar()
    tk.Label(window, text='Atrial Amplitude(mV)').place(x=10, y=200)
    tk.Spinbox(window, state="readonly",values=["OFF"] + list(np.arange(100, 5100, 100)) , width=8,textvariable=v_aa).place(x=150, y=200)

    v_apw = tk.StringVar()
    tk.Label(window, text='Atrial Pules Width').place(x=300, y=200)
    tk.Spinbox(window, state="readonly", values=list(np.arange(1, 31, 1)), width=5,textvariable=v_apw).place(x=450, y=200)

    v_as = tk.StringVar()
    tk.Label(window, text='Atrial Sensitivity').place(x=10, y=300)
    tk.Spinbox(window, state="readonly", values=list(np.arange(0, 5200, 100)),width=8, textvariable=v_as).place(x=150, y=300)

    v_arp = tk.StringVar()
    tk.Label(window, text='ARP').place(x=300, y=300)
    tk.Spinbox(window, state="readonly", values=list(range(150, 510, 10)), width=8, textvariable=v_arp).place(x=450, y=300)

    v_pva = tk.StringVar()
    tk.Label(window, text='PVARP').place(x=10, y=400)
    tk.Spinbox(window, state="readonly", values=list(range(150, 510, 10)), width=8, textvariable=v_pva).place(x=150, y=400)

    v_hy = tk.StringVar()
    tk.Label(window, text='Hysteresis').place(x=300, y=400)
    tk.Spinbox(window, state="readonly",
            values=["OFF"] + list(range(30, 51, 5)) + list(range(51, 90, 1)) + list(range(90, 176, 5)), width=8,
            textvariable=v_hy).place(x=450, y=400)

    v_rs = tk.StringVar()
    tk.Label(window, text='Rate Smoothing').place(x=10, y=500)
    tk.Spinbox(window, state="readonly", values=["OFF"] + list(range(3, 24, 3)) + ['25'], width=8,
            textvariable=v_rs).place(x=150, y=500)

    '''@@@Fetch the input data@@@'''
    def parameter_AAI_get_info():
        entryed_lrl = v_lrl.get()
        entryed_url = v_url.get()
        entryed_aa = v_aa.get()
        entryed_apw = v_apw.get()
        entryed_as = v_as.get()
        entryed_arp = v_arp.get()
        entryed_pva = v_pva.get()
        entryed_hy = v_hy.get()
        entryed_rs = v_rs.get()
        data_update_aai(name,entryed_lrl, entryed_url, entryed_aa, entryed_apw,entryed_as, entryed_arp, entryed_pva,entryed_hy, entryed_rs)

    b1 = tk.Button(window, text='save',command=parameter_AAI_get_info)
    b2 = tk.Button(window, text='back', command=window.destroy)
    b3voo = tk.Button(window, text='Stored View', command=lambda: verify(name))
    b4voo = tk.Button(window, text='Pass to Pacemaker', command=lambda: inputPass(name,"AAI"))
    b3voo.place(x=300, y=500)
    b4voo.place(x=400, y=500)
    b1.place(x=10, y=500)
    b2.place(x=200, y=500)
    b1.pack()
    b2.pack()
    b3voo.pack()
    b4voo.pack()

'''***AAI mode update. Write the data in to the file***'''
def data_update_aai(name,v_lrl, v_url, v_aa, v_apw, v_as, v_arp, v_pva, v_hy, v_rs):
    updateDataGet(name)
    with open('parameters.txt', 'r') as file:  # read a list of lines into data
        data = file.readlines()
        data[rows+2] = "AAI\t" + v_lrl + '\t' + v_url + '\t' + v_aa + '\t' + v_apw + "\t"+ v_as + '\t' + v_arp + '\t'+ v_pva + '\t' + v_hy + '\t' + v_rs + '\n'
    with open('parameters.txt', 'w') as file:
        file.writelines(data)

    messagebox.showinfo("System Message", "Success!")


def parameter_VVI(name):
    window = tk.Toplevel()
    window.title('VVI Mode')
    canvas = tk.Canvas(window,height = 560, width =800)
    canvas.pack()

    tk.Label(window, text='VVI Mode',font = Font_tuple2).place(x=345, y=45)

    v_lrl = tk.StringVar()
    tk.Label(window, text='Lower Rate Limit').place(x=10, y=100)
    tk.Spinbox(window, state="readonly",values=(list(range(30, 50, 5)) + list(range(50, 90, 1)) + list(range(90, 176, 5))), width=8,textvariable=v_lrl).place(x=150, y=100)

    v_url = tk.StringVar()
    tk.Label(window, text='Upper Rate Limit').place(x=300, y=100)
    tk.Spinbox(window, state="readonly", values=list(range(50, 176, 5)), width=8, textvariable=v_url).place(x=450, y=100)

    v_va = tk.StringVar()
    tk.Label(window, text='Ventricular Amplitude(mV)').place(x=10, y=200)
    tk.Spinbox(window, state="readonly",values=["OFF"] + list(np.arange(100, 5100, 100)) , width=8,textvariable=v_va).place(x=150, y=200)

    v_vpw = tk.StringVar()
    tk.Label(window, text='Ventricular Pulse Width').place(x=300, y=200)
    tk.Spinbox(window, state="readonly", values=list(np.arange(1, 31, 1)), width=8,textvariable=v_vpw).place(x=450, y=200)

    v_s = tk.StringVar()
    tk.Label(window, text='Ventricular Sensitivity').place(x=10, y=300)
    tk.Spinbox(window, state="readonly",values=list(np.arange(0, 5100, 100)), width=8, textvariable=v_s).place(x=150, y=300)

    v_vrp = tk.StringVar()
    tk.Label(window, text='VRP').place(x=300, y=300)
    tk.Spinbox(window, state="readonly", values=list(range(150, 510, 10)), width=8, textvariable=v_vrp).place(x=450, y=300)

    v_hy = tk.StringVar()
    tk.Label(window, text='Hysteresis').place(x=10, y=400)
    tk.Spinbox(window, state="readonly",values=["OFF"] + list(range(30, 51, 5)) + list(range(51, 90, 1)) + list(range(90, 176, 5)), width=8,textvariable=v_hy).place(x=150, y=400)

    v_rs = tk.StringVar()
    tk.Label(window, text='Rate Smoothing').place(x=300, y=400)
    tk.Spinbox(window, state="readonly", values=["OFF"] + list(range(3, 24, 3)) + ['25'], width=8,textvariable=v_rs).place(x=450, y=400)

    def parameter_VVI_get_info():
        entryed_lrl = v_lrl.get()
        entryed_url = v_url.get()
        entryed_va = v_va.get()
        entryed_vpw = v_vpw.get()
        entryed_v_s = v_s.get()
        entryed_vrp = v_vrp.get()
        entryed_hy = v_hy.get()
        entryed_rs = v_rs.get()
        data_update_vvi(name,entryed_lrl, entryed_url, entryed_va, entryed_vpw,entryed_v_s,entryed_vrp,entryed_hy,entryed_rs)

    b1 = tk.Button(window, text='save',command=parameter_VVI_get_info)
    b2 = tk.Button( window, text='back', command= window.destroy)
    b3voo = tk.Button(window, text='Stored View', command=lambda: verify(name))
    b4voo = tk.Button(window, text='Pass to Pacemaker', command=lambda: inputPass(name,"VVI"))
    b1.place(x=10, y=500)
    b2.place(x=200, y=500)
    b3voo.place(x=300, y=500)
    b4voo.place(x=400, y=500)
    b1.pack()
    b2.pack()
    b3voo.pack()
    b4voo.pack()

'''***VVI mode update. Write the data in to the file***'''
def data_update_vvi(name,v_lrl, v_url, v_va, v_vpw,v_s,v_vrp,v_hy,v_rs):
    updateDataGet(name)
    with open('parameters.txt', 'r') as file:  # read a list of lines into data
        data = file.readlines()
        data[rows+3] = "VVI\t" + v_lrl + '\t' + v_url + '\t' + v_va + '\t' + v_vpw + "\t"+ v_s + '\t' + v_vrp + '\t' + v_hy + '\t' + v_rs + '\n'
    with open('parameters.txt', 'w') as file:
        file.writelines(data)
    messagebox.showinfo("System Message", "Success!")


def parameter_DOO(name):
    window_Pacemaker = tk.Toplevel()
    window_Pacemaker.title('DOO Mode')
    canvas = tk.Canvas(window_Pacemaker,height = 560, width =800)
    canvas.pack()
    tk.Label(window_Pacemaker, text='DOO Mode',font = Font_tuple2).place(x=345, y=45)

    v_lrl = tk.StringVar()
    LRL = tk.Label(window_Pacemaker, text='Lower Rate Limit').place(x=10, y=100)
    tk.Spinbox(window_Pacemaker, state="readonly",values=(list(range(30, 50, 5)) + list(range(50, 90, 1)) + list(range(90, 176, 5))), width=8, textvariable=v_lrl).place(x=150, y=100)

    v_url = tk.StringVar()
    tk.Label(window_Pacemaker, text='Upper Rate Limit').place(x=250, y=100)
    tk.Spinbox(window_Pacemaker,state="readonly", values=list(range(50,176,5)), width=8, textvariable=v_url).place(x=370, y=100)

    fixedAvDelay = tk.StringVar()
    tk.Label(window_Pacemaker, text='Fixed Av Delay').place(x=10, y=200)
    tk.Spinbox(window_Pacemaker, state="readonly", values=list(range(70, 301, 10)), width=8,textvariable=fixedAvDelay).place(x=150, y=200)

    v_aa = tk.StringVar()
    tk.Label(window_Pacemaker, text='Atrial Amplitude(mV)').place(x=250, y=200)
    tk.Spinbox(window_Pacemaker, state="readonly",values=["OFF"] + list(np.arange(100,5100,100)),width=8,textvariable=v_aa).place(x=370, y=200)

    v_apw = tk.StringVar()
    tk.Label(window_Pacemaker, text='Atrial Pules Width').place(x=10, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly", values= list(np.arange(1, 31, 1)), width=8,textvariable=v_apw).place(x=150, y=300)

    v_va = tk.StringVar()
    tk.Label(window_Pacemaker, text='Ventricular Amplitude(mV)').place(x=250, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly",values=["OFF"] + list(np.arange(100,5100,100)) , width=8,textvariable=v_va).place(x=370, y=300)

    v_vpw = tk.StringVar()
    tk.Label(window_Pacemaker, text='Ventricular Pulse Width').place(x=10, y=400)
    tk.Spinbox(window_Pacemaker, state="readonly", values= list(np.arange(1, 31, 1)), width=8,textvariable=v_vpw).place(x=150, y=400)

    def parameter_DOO_get_info():
        entryed_aa = v_aa.get()
        entryed_apw = v_apw.get()
        entryed_lrl = v_lrl.get()
        entryed_url = v_url.get()
        entryed_fad = fixedAvDelay.get()
        entryed_va = v_va.get()
        entryed_vpw = v_vpw.get()
        data_update_doo(name,entryed_lrl, entryed_url,entryed_fad, entryed_aa,entryed_va, entryed_apw,entryed_vpw)

    b1 = tk.Button(window_Pacemaker, text='save',command= parameter_DOO_get_info)
    b2 = tk.Button(window_Pacemaker, text='back', command=window_Pacemaker.destroy)
    b1.place(x=10, y=500)
    b2.place(x=200, y=500)
    b1.pack()
    b2.pack()
    b3voo = tk.Button(window_Pacemaker, text='Stored View', command=lambda: verify(name))
    b4voo = tk.Button(window_Pacemaker, text='Pass to Pacemaker', command=lambda: inputPass(name,"DOO"))
    b3voo.place(x=300, y=500)
    b4voo.place(x=400, y=500)
    b3voo.pack()
    b4voo.pack()

'''***DOO mode update. Write the data in to the file***'''
def data_update_doo(name,v_lrl, v_url,fixedAvDelay,v_aa,v_va, v_apw,v_vpw):
    updateDataGet(name)
    with open('parameters.txt', 'r') as file:  # read a list of lines into data
        data = file.readlines()
        data[rows+4] = "DOO\t" + v_lrl + '\t' + v_url + '\t' + fixedAvDelay + '\t' + v_aa + "\t"+ v_va+ '\t' + v_apw  + '\t' + v_vpw + '\n'
    with open('parameters.txt', 'w') as file:
        file.writelines(data)
    messagebox.showinfo("System Message", "Success!")


def parameter_AOOR(name):
    window_Pacemaker = tk.Toplevel()
    window_Pacemaker.title('AOOR Mode')
    canvas = tk.Canvas(window_Pacemaker,height = 560, width =800)
    canvas.pack()

    tk.Label(window_Pacemaker, text='AOOR Mode',font = Font_tuple2).place(x=345, y=45)

    v_lrl = tk.StringVar()
    LRL = tk.Label(window_Pacemaker, text='Lower Rate Limit').place(x=10, y=100)
    tk.Spinbox(window_Pacemaker, state="readonly",values=(list(range(30, 50, 5)) + list(range(50, 90, 1)) + list(range(90, 176, 5))),
               width=8, textvariable=v_lrl).place(x=150, y=100)

    v_url = tk.StringVar()
    tk.Label(window_Pacemaker, text='Upper Rate Limit').place(x=270, y=100)
    tk.Spinbox(window_Pacemaker,state="readonly", values=list(range(50,176,5)), width=8, textvariable=v_url).place(x=400, y=100)
    entryed_v_url = v_url.get()

    maxSensorRate= tk.StringVar()
    tk.Label(window_Pacemaker, text='Maximum Sensor Rate').place(x=500, y=100)
    tk.Spinbox(window_Pacemaker, state="readonly", values=list(range(50, 176, 5)), width=8, textvariable=maxSensorRate).place(
        x=650, y=100)


    v_aa = tk.StringVar()
    tk.Label(window_Pacemaker, text='Atrial Amplitude(mV)').place(x=10, y=200)
    tk.Spinbox(window_Pacemaker, state="readonly",values=["OFF"] + list(np.arange(100,5100,100)),
               width=8,textvariable=v_aa).place(x=150, y=200)

    v_apw = tk.StringVar()
    tk.Label(window_Pacemaker, text='Atrial Pules Width').place(x=270, y=200)
    tk.Spinbox(window_Pacemaker, state="readonly", values= list(np.arange(1, 31, 1)), width=8,
            textvariable=v_apw).place(x=400, y=200)

    activityThreshold = tk.StringVar()
    tk.Label(window_Pacemaker, text='Activity Threshold').place(x=500, y=200)
    tk.Spinbox(window_Pacemaker, state="readonly",values=["V-Low", "Low", "Med-Low", "Med", "Med-High", "High", "V-High"],
               width=8,textvariable=activityThreshold).place(x=650, y=200)

    reactionTime = tk.StringVar()
    tk.Label(window_Pacemaker, text='Reaction Time').place(x=10, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly", value=list(range(10, 60, 10)), width=8,
                           textvariable=reactionTime).place(x=150, y=300)

    responseFactor = tk.StringVar()
    tk.Label(window_Pacemaker, text='Response Factor').place(x=270, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly", value=list(range(1, 17, 1)), width=8,
                           textvariable=responseFactor).place(x=400, y=300)

    recoveryTime = tk.StringVar()
    tk.Label(window_Pacemaker, text='Recovery Time').place(x=500, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly", value=list(range(2, 17, 1)), width=8,
                           textvariable=recoveryTime).place(x=650, y=300)


    def parameter_AOOR_get_info():
        entryed_aa = v_aa.get()
        entryed_apw = v_apw.get()
        entryed_lrl = v_lrl.get()
        entryed_url = v_url.get()
        entryed_maxSensorRate = maxSensorRate.get()
        entryed_activityThreshold = activityThreshold.get()
        entryed_reactionTime = reactionTime.get()
        entryed_responseFactor = responseFactor.get()
        entryed_recoveryTime = recoveryTime.get()
        data_update_aoor(name,entryed_lrl, entryed_url, entryed_maxSensorRate,entryed_aa, entryed_apw,entryed_activityThreshold,entryed_reactionTime,
                         entryed_responseFactor,entryed_recoveryTime)

    b1 = tk.Button(window_Pacemaker, text='save',
                   command= parameter_AOOR_get_info)
    b2 = tk.Button(window_Pacemaker, text='back', command=window_Pacemaker.destroy)
    b1.place(x=10, y=500)
    b2.place(x=200, y=500)
    b1.pack()
    b2.pack()
    b3voo = tk.Button(window_Pacemaker, text='Stored View', command=lambda: verify(name))
    b4voo = tk.Button(window_Pacemaker, text='Pass to Pacemaker', command=lambda: inputPass(name,"AOOR"))
    b3voo.place(x=300, y=500)
    b4voo.place(x=400, y=500)
    b3voo.pack()
    b4voo.pack()


'''***AOOR mode update. Write the data in to the file***'''
def data_update_aoor(name,lrl, url,maxSensorRate, entryed_aa, apw,activityThreshold,reactionTime,responseFactor,recoveryTime):
    updateDataGet(name)
    with open('parameters.txt', 'r') as file:  # read a list of lines into data
        data = file.readlines()
        data[rows+5] = "AOOR\t" + lrl+ '\t' + url + '\t' + maxSensorRate + '\t' + entryed_aa+ '\t' + apw+ "\t"+ activityThreshold+ '\t' + reactionTime+ '\t'+ responseFactor+ '\t'+ recoveryTime+ '\n'
    with open('parameters.txt', 'w') as file:
        file.writelines(data)
    messagebox.showinfo("System Message", "Success!")


def parameter_VOOR(name):
    window_Pacemaker = tk.Toplevel()
    window_Pacemaker.title('VOOR Mode')
    canvas = tk.Canvas(window_Pacemaker,height = 560, width =800)
    canvas.pack()

    tk.Label(window_Pacemaker, text='VOOR Mode',font = Font_tuple2).place(x=345, y=45)

    v_lrl = tk.StringVar()
    LRL = tk.Label(window_Pacemaker, text='Lower Rate Limit').place(x=10, y=100)
    tk.Spinbox(window_Pacemaker, state="readonly",
               values=(list(range(30, 50, 5)) + list(range(50, 90, 1)) + list(range(90, 176, 5))), width=8, textvariable=v_lrl).place(x=150, y=100)
    entryed_v_lrl = v_lrl.get()

    v_lrl = tk.StringVar()
    LRL = tk.Label(window_Pacemaker, text='Lower Rate Limit').place(x=10, y=100)
    tk.Spinbox(window_Pacemaker, state="readonly",
               values=(list(range(30, 50, 5)) + list(range(50, 90, 1)) + list(range(90, 176, 5))),
               width=8, textvariable=v_lrl).place(x=150, y=100)

    v_url = tk.StringVar()
    tk.Label(window_Pacemaker, text='Upper Rate Limit').place(x=270, y=100)
    tk.Spinbox(window_Pacemaker, state="readonly", values=list(range(50, 176, 5)), width=8, textvariable=v_url).place(
        x=400, y=100)

    maxSensorRate = tk.StringVar()
    tk.Label(window_Pacemaker, text='Maximum Sensor Rate').place(x=500, y=100)
    tk.Spinbox(window_Pacemaker, state="readonly", values=list(range(50, 176, 5)), width=8,
               textvariable=maxSensorRate).place(x=650, y=100)

    v_va = tk.StringVar()
    tk.Label(window_Pacemaker, text='Vertricular Amplitude').place(x=10, y=200)
    tk.Spinbox(window_Pacemaker,state="readonly", values=["OFF"] + list(np.arange(100,5100,100)), width=8,
               textvariable=v_va).place(x=150, y=200)

    v_vpw = tk.StringVar()
    tk.Label(window_Pacemaker, text='Ventricular Pules Width').place(x=270, y=200)
    tk.Spinbox(window_Pacemaker, state="readonly", values= list(np.arange(1, 31, 1)), width=8,
               textvariable=v_vpw).place(x=400, y=200)

    activityThreshold = tk.StringVar()
    tk.Label(window_Pacemaker, text='Activity Threshold').place(x=500, y=200)
    tk.Spinbox(window_Pacemaker, state="readonly",
               values=["V-Low", "Low", "Med-Low", "Med", "Med-High", "High", "V-High"],
               width=8, textvariable=activityThreshold).place(x=650, y=200)

    reactionTime = tk.StringVar()
    tk.Label(window_Pacemaker, text='Reaction Time').place(x=10, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly", value=list(range(10, 60, 10)), width=8,
               textvariable=reactionTime).place(x=150, y=300)

    responseFactor = tk.StringVar()
    tk.Label(window_Pacemaker, text='Response Factor').place(x=270, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly", value=list(range(1, 17, 1)), width=8,
               textvariable=responseFactor).place(x=400, y=300)

    recoveryTime = tk.StringVar()
    tk.Label(window_Pacemaker, text='Recovery Time').place(x=500, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly", value=list(range(2, 17, 1)), width=8,
               textvariable=recoveryTime).place(x=650, y=300)

    def parameter_VOOR_get_info():
        entryed_va = v_va.get()
        entryed_vpw = v_vpw.get()
        entryed_lrl = v_lrl.get()
        entryed_url = v_url.get()
        entryed_maxSensorRate = maxSensorRate.get()
        entryed_activityThreshold = activityThreshold.get()
        entryed_reactionTime = reactionTime.get()
        entryed_responseFactor = responseFactor.get()
        entryed_recoveryTime = recoveryTime.get()
        data_update_voor(name,entryed_lrl, entryed_url,entryed_maxSensorRate, entryed_va, entryed_vpw,entryed_activityThreshold,entryed_reactionTime,
                         entryed_responseFactor,entryed_recoveryTime)

    b1 = tk.Button(window_Pacemaker, text='save',
                   command= parameter_VOOR_get_info)
    b2 = tk.Button(window_Pacemaker, text='back', command=window_Pacemaker.destroy)
    b1.place(x=10, y=500)
    b2.place(x=200, y=500)
    b1.pack()
    b2.pack()
    b3voo = tk.Button(window_Pacemaker, text='Stored View', command=lambda: verify(name))
    b4voo = tk.Button(window_Pacemaker, text='Pass to Pacemaker', command=lambda: inputPass(name,"VOOR"))
    b3voo.place(x=300, y=500)
    b4voo.place(x=400, y=500)
    b3voo.pack()
    b4voo.pack()

'''***VOOR mode update. Write the data in to the file***'''
def data_update_voor(name,lrl, url,maxSensorRate, va, vpw,activityThreshold,reactionTime,entryed_responseFactor,entryed_recoveryTime):
    updateDataGet(name)
    with open('parameters.txt', 'r') as file:  # read a list of lines into data
        data = file.readlines()
        data[rows+6] = "VOOR\t" + lrl + '\t' + url + '\t'+ va +'\t' + vpw+ "\t"\
                     + maxSensorRate+ '\t' + activityThreshold+ '\t' + reactionTime+ '\t'\
                     + entryed_responseFactor+ '\t'+ entryed_recoveryTime+ '\n'
    with open('parameters.txt', 'w') as file:
        file.writelines(data)
    messagebox.showinfo("System Message", "Success!")

def parameter_AAIR(name):
    window_Pacemaker = tk.Toplevel()
    window_Pacemaker.title('AAIR Mode')
    canvas = tk.Canvas(window_Pacemaker,height = 560, width =800)
    canvas.pack()

    tk.Label(window_Pacemaker, text='AAIR Mode',font = Font_tuple2).place(x=345, y=45)

    v_lrl = tk.StringVar()
    LRL = tk.Label(window_Pacemaker, text='Lower Rate Limit').place(x=10, y=100)
    tk.Spinbox(window_Pacemaker, state="readonly",values=(list(range(30, 50, 5)) + list(range(50, 90, 1)) + list(range(90, 176, 5))), width=8,
               textvariable=v_lrl).place(x=150, y=100)

    v_url = tk.StringVar()
    tk.Label(window_Pacemaker, text='Upper Rate Limit').place(x=270, y=100)
    tk.Spinbox(window_Pacemaker,state="readonly", values=list(range(50,176,5)), width=8, textvariable=v_url).place(x=400, y=100)

    maximumSensorRate = tk.StringVar()
    tk.Label(window_Pacemaker, text='Maximum Sensor Rate').place(x=500, y=100)
    tk.Spinbox(window_Pacemaker,state="readonly", values=list(range(50,176,5)), width=8, textvariable=maximumSensorRate).place(x=650, y=100)

    v_aa = tk.StringVar()
    tk.Label(window_Pacemaker, text='Atrial Amplitude(mV)').place(x=10, y=200)
    tk.Spinbox(window_Pacemaker, state="readonly",values=["OFF"] + list(np.arange(100,5100,100)),
               width=8,textvariable=v_aa).place(x=150, y=200)

    v_apw = tk.StringVar()
    tk.Label(window_Pacemaker, text='Atrial Pules Width').place(x=270, y=200)
    tk.Spinbox(window_Pacemaker, state="readonly", values= list(np.arange(1, 31, 1)), width=8,
            textvariable=v_apw).place(x=400, y=200)

    AtrialSensitivity = tk.StringVar()
    tk.Label(window_Pacemaker, text='Atrial Sensitivity(mV)').place(x=500, y=200)
    tk.Spinbox(window_Pacemaker, state="readonly", values=[0, 5100, 100], width=8,
               textvariable=AtrialSensitivity).place(x=650, y=200)

    ARP = tk.StringVar()
    tk.Label(window_Pacemaker, text='ARP ').place(x=10, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly", values=list(range(150,510,10)), width=8, textvariable=ARP).place(x=150, y=300)

    PVARP = tk.StringVar()
    tk.Label(window_Pacemaker, text='PVARP').place(x=270, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly", values=["OFF"] + list(range(50, 450, 50)), width=8,textvariable=PVARP).place(x=400, y=300)

    v_hy = tk.StringVar()
    tk.Label(window_Pacemaker, text='Hysteresis').place(x=500, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly",
               values=["OFF"] + list(range(30, 51, 5)) + list(range(51, 90, 1)) + list(range(90, 176, 5)), width=8,
               textvariable=v_hy).place(x=650, y=300)

    v_rs = tk.StringVar()
    tk.Label(window_Pacemaker, text='Rate Smoothing').place(x=10, y=400)
    tk.Spinbox(window_Pacemaker, state="readonly", values=["OFF"] + list(range(3, 24, 3)) + ['25'], width=8,
               textvariable=v_rs).place(x=150, y=400)

    activityThreshold = tk.StringVar()
    tk.Label(window_Pacemaker, text='Activity Threshold').place(x=270, y=400)
    tk.Spinbox(window_Pacemaker, state="readonly",values=["V-Low", "Low", "Med-Low", "Med", "Med-High", "High", "V-High"],
               width=8,textvariable=activityThreshold).place(x=400, y=400)

    reactionTime = tk.StringVar()
    tk.Label(window_Pacemaker, text='Reaction Time').place(x=500, y=400)
    tk.Spinbox(window_Pacemaker, state="readonly", value=list(range(10, 60, 10)), width=8,
                           textvariable=reactionTime).place(x=650, y=400)

    responseFactor = tk.StringVar()
    tk.Label(window_Pacemaker, text='Response Factor').place(x=10, y=500)
    tk.Spinbox(window_Pacemaker, state="readonly", value=list(range(1, 17, 1)), width=8,
                           textvariable=responseFactor).place(x=150, y=500)

    recoveryTime = tk.StringVar()
    tk.Label(window_Pacemaker, text='Recovery Time').place(x=270, y=500)
    tk.Spinbox(window_Pacemaker, state="readonly", value=list(range(2, 17, 1)), width=8,
                           textvariable=recoveryTime).place(x=400, y=500)

    def parameter_AAIR_get_info():
        entryed_aa = v_aa.get()
        entryed_apw = v_apw.get()
        entryed_lrl = v_lrl.get()
        entryed_url = v_url.get()
        entryed_msr = maximumSensorRate.get()
        entryed_as = AtrialSensitivity.get()
        entryed_ARP = ARP.get()
        entryed_PVARP = PVARP.get()
        entryed_v_hy= v_hy.get()
        entryed_v_rs = v_rs.get()
        entryed_activityThreshold = activityThreshold.get()
        entryed_reactionTime = reactionTime.get()
        entryed_responseFactor = responseFactor.get()
        entryed_recoveryTime = recoveryTime.get()
        data_update_aair(name,entryed_lrl, entryed_url,entryed_msr, entryed_aa, entryed_apw,entryed_as,entryed_ARP,
                     entryed_PVARP,entryed_v_hy,entryed_v_rs,entryed_activityThreshold,entryed_reactionTime,
                     entryed_responseFactor,entryed_recoveryTime)

    b1 = tk.Button(window_Pacemaker, text='save',
                   command= parameter_AAIR_get_info)
    b2 = tk.Button(window_Pacemaker, text='back', command=window_Pacemaker.destroy)
    b1.place(x=10, y=500)
    b2.place(x=200, y=500)
    b1.pack()
    b2.pack()
    b3voo = tk.Button(window_Pacemaker, text='Stored View', command=lambda: verify(name))
    b4voo = tk.Button(window_Pacemaker, text='Pass to Pacemaker', command=lambda: inputPass(name,"AAIR"))
    b3voo.place(x=300, y=500)
    b4voo.place(x=400, y=500)
    b3voo.pack()
    b4voo.pack()

'''***AAIR mode update. Write the data in to the file***'''
def data_update_aair(name,lrl, url, msr,aa, apw,entryed_as,entryed_ARP,
                     entryed_PVARP,entryed_v_hy,entryed_v_rs,entryed_activityThreshold,entryed_reactionTime,
                     entryed_responseFactor,entryed_recoveryTime):
    updateDataGet(name)
    with open('parameters.txt', 'r') as file:  # read a list of lines into data
        data = file.readlines()
        data[rows+7] = "AAIR\t" + lrl+ '\t' +url+ '\t'+ msr+'\t'+ aa+'\t' + apw+ '\t' + entryed_as+'\t' + entryed_ARP+'\t'+ entryed_PVARP\
                     +'\t'+ entryed_v_hy+'\t'+ entryed_v_rs + '\t'+ entryed_activityThreshold+ '\t' + entryed_reactionTime+ '\t'\
                     + entryed_responseFactor+ '\t'+ entryed_recoveryTime+ '\n'
    with open('parameters.txt', 'w') as file:
        file.writelines(data)
    messagebox.showinfo("System Message", "Success!")

def parameter_VVIR(name):
    window_Pacemaker = tk.Toplevel()
    window_Pacemaker.title('VVIR Mode')
    canvas = tk.Canvas(window_Pacemaker,height = 560, width =800)
    canvas.pack()

    tk.Label(window_Pacemaker, text='VVIR Mode',font = Font_tuple2).place(x=345, y=45)


    v_lrl = tk.StringVar()
    LRL = tk.Label(window_Pacemaker, text='Lower Rate Limit').place(x=10, y=100)
    tk.Spinbox(window_Pacemaker, state="readonly",
               values=(list(range(30, 50, 5)) + list(range(50, 90, 1)) + list(range(90, 176, 5))), width=8, textvariable=v_lrl).place(x=150, y=100)

    v_url = tk.StringVar()
    tk.Label(window_Pacemaker, text='Upper Rate Limit').place(x=270, y=100)
    tk.Spinbox(window_Pacemaker,state="readonly", values=list(range(50,176,5)), width=8, textvariable=v_url).place(x=400, y=100)

    maximumSensorRate = tk.StringVar()
    tk.Label(window_Pacemaker, text='Maximum Sensor Rate').place(x=500, y=100)
    tk.Spinbox(window_Pacemaker,state="readonly", values=list(range(50,176,5)), width=8, textvariable=maximumSensorRate).place(x=650, y=100)

    v_va = tk.StringVar()
    tk.Label(window_Pacemaker, text='Vertricular Amplitude').place(x=10, y=200)
    tk.Spinbox(window_Pacemaker,state="readonly", values=["OFF"] + list(np.arange(100,5100,100)), width=8,
               textvariable=v_va).place(x=150, y=200)

    v_vpw = tk.StringVar()
    tk.Label(window_Pacemaker, text='Ventricular Pules Width').place(x=270, y=200)
    tk.Spinbox(window_Pacemaker, state="readonly", values= list(np.arange(1, 31, 1)), width=8,
               textvariable=v_vpw).place(x=400, y=200)

    VentricularSensitivity = tk.StringVar()
    tk.Label(window_Pacemaker, text='Ventricular Sensitivity(mV)').place(x=500, y=200)
    tk.Spinbox(window_Pacemaker, state="readonly", values=[0, 5100, 100], width=8,
               textvariable=VentricularSensitivity).place(x=650, y=200)

    VRP = tk.StringVar()
    tk.Label(window_Pacemaker, text='VRP ').place(x=10, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly", values=list(range(150,510,10)), width=8, textvariable=VRP).place(x=150, y=300)

    v_hy = tk.StringVar()
    tk.Label(window_Pacemaker, text='Hysteresis').place(x=270, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly",
               values=["OFF"] + list(range(30, 51, 5)) + list(range(51, 90, 1)) + list(range(90, 176, 5)), width=8,
               textvariable=v_hy).place(x=400, y=300)

    v_rs = tk.StringVar()
    tk.Label(window_Pacemaker, text='Rate Smoothing').place(x=500, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly", values=["OFF"] + list(range(3, 24, 3)) + ['25'], width=8,
               textvariable=v_rs).place(x=650, y=300)

    activityThreshold = tk.StringVar()
    tk.Label(window_Pacemaker, text='Activity Threshold').place(x=10, y=400)
    tk.Spinbox(window_Pacemaker, state="readonly",values=["V-Low", "Low", "Med-Low", "Med", "Med-High", "High", "V-High"],
               width=8,textvariable=activityThreshold).place(x=150, y=400)

    reactionTime = tk.StringVar()
    tk.Label(window_Pacemaker, text='Reaction Time').place(x=270, y=400)
    tk.Spinbox(window_Pacemaker, state="readonly", value=list(range(10, 60, 10)), width=8,
                           textvariable=reactionTime).place(x=400, y=400)

    responseFactor = tk.StringVar()
    tk.Label(window_Pacemaker, text='Response Factor').place(x=500, y=400)
    tk.Spinbox(window_Pacemaker, state="readonly", value=list(range(1, 17, 1)), width=8,
                           textvariable=responseFactor).place(x=650, y=400)

    recoveryTime = tk.StringVar()
    tk.Label(window_Pacemaker, text='Recovery Time').place(x=10, y=500)
    tk.Spinbox(window_Pacemaker, state="readonly", value=list(range(2, 17, 1)), width=8,
                           textvariable=recoveryTime).place(x=150, y=500)

    def parameter_VVIR_get_info():
        entryed_va = v_va.get()
        entryed_vpw = v_vpw.get()
        entryed_lrl = v_lrl.get()
        entryed_url = v_url.get()
        entryed_msr = maximumSensorRate.get()
        entryed_vs = VentricularSensitivity.get()
        entryed_VRP = VRP.get()
        entryed_v_hy= v_hy.get()
        entryed_v_rs = v_rs.get()
        entryed_activityThreshold = activityThreshold.get()
        entryed_reactionTime = reactionTime.get()
        entryed_responseFactor = responseFactor.get()
        entryed_recoveryTime = recoveryTime.get()
        data_update_vvir(name,entryed_lrl, entryed_url, entryed_msr,entryed_va, entryed_vpw,entryed_vs,entryed_VRP,
                     entryed_v_hy,entryed_v_rs,entryed_activityThreshold,entryed_reactionTime,
                     entryed_responseFactor,entryed_recoveryTime)

    b1 = tk.Button(window_Pacemaker, text='save',
                   command= parameter_VVIR_get_info)
    b2 = tk.Button(window_Pacemaker, text='back', command=window_Pacemaker.destroy)
    b1.place(x=10, y=500)
    b2.place(x=200, y=500)
    b1.pack()
    b2.pack()
    b3voo = tk.Button(window_Pacemaker, text='Stored View', command=lambda: verify(name))
    b4voo = tk.Button(window_Pacemaker, text='Pass to Pacemaker', command=lambda: inputPass(name,"VVIR"))
    b3voo.place(x=300, y=500)
    b4voo.place(x=400, y=500)
    b3voo.pack()
    b4voo.pack()

'''***VVIR mode update. Write the data in to the file***'''
def data_update_vvir(name,lrl, url,msr, va, vpw,vs,VRP,
                     entryed_v_hy,entryed_v_rs,entryed_activityThreshold,entryed_reactionTime,
                     entryed_responseFactor,entryed_recoveryTime):
    updateDataGet(name)
    with open('parameters.txt', 'r') as file:  # read a list of lines into data
        data = file.readlines()
        data[rows+8] = "VVIR\t" + lrl+ '\t' +url+'\t'+ msr+'\t' + va+'\t' + vpw+ '\t'+ vs+'\t' + VRP+'\t'\
                     +'\t'+ entryed_v_hy+'\t'+ entryed_v_rs + '\t'+ entryed_activityThreshold+ '\t' \
                     + entryed_reactionTime+ '\t'+ entryed_responseFactor+ '\t'+ entryed_recoveryTime+ '\n'
    with open('parameters.txt', 'w') as file:
        file.writelines(data)
    messagebox.showinfo("System Message", "Success!")


def parameter_DOOR(name):
    window_Pacemaker = tk.Toplevel()
    window_Pacemaker.title('DOOR Mode')
    canvas = tk.Canvas(window_Pacemaker,height = 560, width =800)
    canvas.pack()

    tk.Label(window_Pacemaker, text='DOOR Mode',font = Font_tuple2).place(x=345, y=45)
    v_lrl = tk.StringVar()
    LRL = tk.Label(window_Pacemaker, text='Lower Rate Limit').place(x=10, y=100)
    tk.Spinbox(window_Pacemaker, state="readonly",
               values=(list(range(30, 50, 5)) + list(range(50, 90, 1)) + list(range(90, 176, 5))), width=8, textvariable=v_lrl).place(x=150, y=100)

    v_url = tk.StringVar()
    tk.Label(window_Pacemaker, text='Upper Rate Limit').place(x=270, y=100)
    tk.Spinbox(window_Pacemaker,state="readonly", values=list(range(50,176,5)), width=8, textvariable=v_url).place(x=400, y=100)

    maximumSensorRate = tk.StringVar()
    tk.Label(window_Pacemaker, text='Maximum Sensor Rate').place(x=500, y=100)
    tk.Spinbox(window_Pacemaker,state="readonly", values=list(range(50,176,5)), width=8, textvariable=maximumSensorRate).place(x=650, y=100)

    FixedAVDelay = tk.StringVar()
    tk.Label(window_Pacemaker, text='Fixed AV Delay').place(x=10, y=200)
    tk.Spinbox(window_Pacemaker, state="readonly", values=list(range(70,301,10)), width=8,
               textvariable=FixedAVDelay).place(x=150, y=200)

    v_aa = tk.StringVar()
    tk.Label(window_Pacemaker, text='Atrial Amplitude(mV)').place(x=270, y=200)
    tk.Spinbox(window_Pacemaker, state="readonly",
               values=["OFF"] + list(np.arange(100, 5100, 100)) ,
               width=8, textvariable=v_aa).place(x=400, y=200)

    v_apw = tk.StringVar()
    tk.Label(window_Pacemaker, text='Atrial Pules Width').place(x=500, y=200)
    tk.Spinbox(window_Pacemaker, state="readonly", values= list(np.arange(1, 31, 1)), width=8,
               textvariable=v_apw).place(x=650, y=200)

    v_va = tk.StringVar()
    tk.Label(window_Pacemaker, text='Ventricular Amplitude(mV)').place(x=10, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly",
               values=["OFF"] + list(np.arange(100,5100,100)) , width=8,
               textvariable=v_va).place(x=150, y=300)

    v_vpw = tk.StringVar()
    tk.Label(window_Pacemaker, text='Ventricular Pulse Width').place(x=270, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly", values= list(np.arange(1, 31, 1)), width=8,textvariable=v_vpw).place(x=400, y=300)

    activityThreshold = tk.StringVar()
    tk.Label(window_Pacemaker, text='Activity Threshold').place(x=500, y=300)
    tk.Spinbox(window_Pacemaker, state="readonly",values=["V-Low", "Low", "Med-Low", "Med", "Med-High", "High", "V-High"],
               width=8,textvariable=activityThreshold).place(x=650, y=300)

    reactionTime = tk.StringVar()
    tk.Label(window_Pacemaker, text='Reaction Time').place(x=10, y=400)
    tk.Spinbox(window_Pacemaker, state="readonly", value=list(range(10, 60, 10)), width=8,textvariable=reactionTime).place(x=150, y=400)

    responseFactor = tk.StringVar()
    tk.Label(window_Pacemaker, text='Response Factor').place(x=270, y=400)
    tk.Spinbox(window_Pacemaker, state="readonly", value=list(range(1, 17, 1)), width=8,textvariable=responseFactor).place(x=400, y=400)

    recoveryTime = tk.StringVar()
    tk.Label(window_Pacemaker, text='Recovery Time').place(x=500, y=400)
    tk.Spinbox(window_Pacemaker, state="readonly", value=list(range(2, 17, 1)), width=8,textvariable=recoveryTime).place(x=650, y=400)

    def parameter_DOOR_get_info():
        entryed_lrl = v_lrl.get()
        entryed_url = v_url.get()
        entryed_msr = maximumSensorRate.get()
        entryed_fad = FixedAVDelay.get()
        entryed_aa = v_aa.get()
        entryed_va = v_va.get()
        entryed_apw = v_apw.get()
        entryed_vpw = v_vpw.get()
        entryed_activityThreshold = activityThreshold.get()
        entryed_reactionTime = reactionTime.get()
        entryed_responseFactor = responseFactor.get()
        entryed_recoveryTime = recoveryTime.get()
        data_update_door(name,entryed_lrl, entryed_url,entryed_msr,entryed_fad,entryed_aa,entryed_va,entryed_apw,entryed_vpw,entryed_activityThreshold,entryed_reactionTime,
                     entryed_responseFactor,entryed_recoveryTime)

    b1 = tk.Button(window_Pacemaker, text='save',
                   command= parameter_DOOR_get_info)
    b2 = tk.Button(window_Pacemaker, text='back', command=window_Pacemaker.destroy)
    b1.place(x=10, y=500)
    b2.place(x=200, y=500)
    b1.pack()
    b2.pack()
    b3voo = tk.Button(window_Pacemaker, text='Stored View', command=lambda: verify(name))
    b4voo = tk.Button(window_Pacemaker, text='Pass to Pacemaker', command=lambda: inputPass(name,"DOOR"))
    b3voo.place(x=300, y=500)
    b4voo.place(x=400, y=500)
    b3voo.pack()
    b4voo.pack()

'''***DOOR mode update. Write the data in to the file***'''
def data_update_door(name,lrl, url,msr,fad,aa,va,apw,
                     vpw,entryed_activityThreshold,entryed_reactionTime,
                     entryed_responseFactor,entryed_recoveryTime):
    updateDataGet(name)
    with open('parameters.txt', 'r') as file:
        data = file.readlines()
        data[rows+9] = "DOOR\t" + lrl+ '\t' +url+ '\t'+ msr+'\t' +fad+'\t' + aa+'\t' + va+'\t'+ apw +'\t'+ vpw+'\t'+ entryed_activityThreshold+ '\t' \
                     + entryed_reactionTime+ '\t'+ entryed_responseFactor+ '\t'+ entryed_recoveryTime+ '\n'
    with open('parameters.txt', 'w') as file:
        file.writelines(data)
    messagebox.showinfo("System Message", "Success!")