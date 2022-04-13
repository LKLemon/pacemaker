import tkinter as tk
from parameter_Modifier import *
from Error_msg import *
from serialC import *
import serial
from serial.tools import list_ports
"""
Module: Login & Sign-up window
Description: Create a login window and allow user to regiester and login as existed user. Auto form a sample data set for new user
"""
def main_window():

    global window,v_usr,v_pwd
    window = tk.Tk()
    window.title('PM Log in')

    canvas = tk.Canvas(window, height=80, width=100)
    canvas.grid(column=100, row=60)

    label_main= tk.Label(window, text='WELCOME\n TO\n PACEMAKER',font = Font_tuple)
    label1 = tk.Label(window, text='USERNAME：')
    label2 = tk.Label(window, text='PASSWORD：')
    label_main.grid(column=53, row=0)
    label1.grid(column=50, row=15)
    label2.grid(column=50, row=17)

    v_usr = tk.StringVar()
    v_pwd = tk.StringVar()
    entry_usr = tk.Entry(window, textvariable=v_usr, width=20)
    entry_pwd = tk.Entry(window, textvariable=v_pwd, show="*", width=20)
    entry_usr.grid(column = 53, row = 15)
    entry_pwd.grid(column = 53, row = 17)
    b1 = tk.Button(window, text='Sign in', command=get_information)
    b2 = tk.Button(window, text='Exit', command=window.quit)
    b3 = tk.Button(window, text='Sign up', command=sign_up)
    b1.grid(column = 53, row = 25)
    b2.grid(column=53, row=27)
    b3.grid(column=53, row=29)

    window.mainloop()


def get_information():
    global name,pwd
    name = v_usr.get()
    pwd = v_pwd.get()
    print("username：{0}   password：{1}".format(name, pwd))
    loginGo(name, pwd)

def sample_para():

    myVarList = ["AOO","VOO","AAI","VVI","DOO","AOOR","VOOR","AAIR","VVIR","DOOR"]
    file_para = open("parameters.txt", 'a')
    file_para.write(name+'\n')  # append uName and pass to file
    file_para.write(myVarList[0] +'\t60\t120\t5\t1\n')
    file_para.write(myVarList[1] + '\t60\t120\t3.5\t1\n')
    file_para.write(myVarList[2] + '\t60\t120\t5\t1\t-\t250\t250\tOff\tOff\n')
    file_para.write(myVarList[3] + '\t60\t120\t5\t1\t-\t320\tOff\tOff\n')
    file_para.write(myVarList[4] + '\t60\t120\t150\t5\t5\t1\t1\n')
    file_para.write(myVarList[5] + '\t60\t120\t120\t5\t1\t3500\t30\t8\t5\n')
    file_para.write(myVarList[6] + '\t60\t120\t120\t5\t1\t-\t250\t250\tOff\tOff\t3500\t30\t8\t5\n')
    file_para.write(myVarList[7] + '\t60\t120\t120\t5\t1\t3500\t30\t8\t5\n')
    file_para.write(myVarList[8] + '\t60\t120\t120\t5\t1\t-\t320\tOff\tOff\t3500\t30\t8\t5\n')
    file_para.write(myVarList[9] + '\t60\t120\t120\t150\t5\t5\t1\t1\t3500\t30\t8\t5\n')
    file_para.close()

def sign_up():
    def sign_up_get_info():
        global name
        name = new_usr.get()
        pwd = new_pwd.get()
        confirm_pwd = new_pwd_confirm.get()
        print("username：{0}   password：{1}".format(name, pwd))
        registerUser(name, pwd, confirm_pwd)

    window_sign_up = tk.Toplevel(window)
    window_sign_up.title('Sign up')
    canvas = tk.Canvas(window_sign_up, height=200, width=350)
    canvas.pack()

    new_usr = tk.StringVar()
    tk.Label(window_sign_up, text='Username:').place(x=10, y=10)
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_usr)
    entry_new_name.place(x=150, y=10)

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='Password:').place(x=10, y=50)
    entry_new_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_new_pwd.place(x=150, y=50)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='Confirm password:').place(x=10, y=90)
    entry_comfirm_sign_up = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_comfirm_sign_up.place(x=150, y=90)

    btn_comfirm_sign_up = tk.Button(window_sign_up, text='Sign up', command=sign_up_get_info)
    btn_comfirm_sign_up.place(x = 150,y = 130)
    btn_comfirm_sign_up.pack()
    b2 = tk.Button(window_sign_up, text='Exit', command=window_sign_up.destroy)
    b2.place(x=150, y=150)
    b2.pack()

def registerUser(uName, p1, p2):
    print("u"+uName)
    if((uName==" " ) or (p1==" ") or (p2=="" )or (uName == "")):
        messagebox.showinfo("System Message", "Invaild input, please enter vaild username and passord!")

    else:
        file = open("users.txt", "r")
        rows = 0
        lines = file.readlines()  # make a list where each line of the file is an index in the list
        if(len(lines)!=0):
            for i in lines:
                rows = rows + 1
                stripped = i.strip("\n")
                FName, FPass = stripped.split("\t")
                if(uName == FName):
                    repeat_user()

        if (p1 == p2):
            print("passwords match")
            print(rows)
            if (rows < 10):  # append the new password and username
                file.close()
                file = open("users.txt", 'a')
                file.write(uName + '\t')  # append uName and pass to file
                file.write(p2 + "\n")
                file.close()
                sample_para()
                messagebox.showinfo("System Message","Suceess!")
            else:
                messagebox.showinfo("System Message","Maximum number of users has been registered!")
                file.close()
        else:
            messagebox.showinfo("System Message","Passwords do not match!")
            file.close()


def loginGo(uName, Pass):
    uName = v_usr.get()
    Pass = v_pwd.get()
    k=0
    if(uName == "" or Pass == ""):
        messagebox.showinfo("System Message", "Invaild input, please enter vaild username and passord!")
    else:
        file = open("users.txt", "r")
        lines = file.readlines()
        if (len(lines)!=0):
            for i in lines:
                stripped = i.strip("\n")
                FName, FPass = stripped.split("\t")
                k+=1
                if (uName == FName) and (Pass == FPass):
                    window.destroy()
                    pacemaker()
                    break
                elif(k==len(lines) or (uName != FName) or (Pass != FPass)):
                    messagebox.showinfo("System Message", "Username and password do not match")
            file.close()
        else:
            messagebox.showinfo("System Message", "Invaild input, please enter vaild username and passord!")

"""
Module: Pacemaker Main Screen
Description: Create a window for pacemaker that can choose to connect and disconnot the device. Display the basic function for 
the pacemaker. Mode selection is availiable when port is connected
"""
def pacemaker():
    global window_pc
    window_pc = tk.Tk()
    window_pc.title('PacemakerMain')
    canvas = tk.Canvas(window_pc,height = 200, width =100)
    canvas.grid(column=60, row=40)
    global connect_bt,refresh

    #Create a drop down menu for detected ports, updata the available ports
    def update_coms():
        global ports,drop_COM,clicked_com
        ports = serial.tools.list_ports.comports()
        coms = [com[0] for com in ports]
        coms.insert(0, "-")

        clicked_com = StringVar()
        clicked_com.set(coms[0])
        drop_COM = OptionMenu(window_pc, clicked_com, *coms,command= connect_check)
        drop_COM.config(width=8)
        drop_COM.grid(column=32, row=30)

    uName = v_usr.get()
    label = tk.Label(window_pc, text='Pacemaker Profile',font = Font_tuple)
    label.grid(column=40, row=5)
    label =tk.Label(window_pc, text='Username:')
    label.grid(column=30, row=25)
    label =tk.Label(window_pc, text= uName)
    label.grid(column=32, row=25)
    label =tk.Label(window_pc, text='Current Device:')
    label.grid(column=30, row=30)
    refresh = tk.Button(window_pc, text='Refresh', command=update_coms)
    refresh.grid(column=32, row=36)
    connect_bt = tk.Button(window_pc, text='Connect', state = "disabled",command=connexion)
    connect_bt.grid(column=33, row=36)

    b1 = tk.Button(window_pc, text='AOO', state = 'disable',command=lambda:parameter_AOO(uName))
    b2 = tk.Button(window_pc, text='VOO', state = 'disable',command=lambda:parameter_VOO(uName))
    b3 = tk.Button(window_pc, text='AAI', state = 'disable',command=lambda:parameter_AAI(uName))
    b4 = tk.Button(window_pc, text='VVI', state = 'disable',command=lambda:parameter_VVI(uName))
    b5 = tk.Button(window_pc, text='DOO', state = 'disable',command=lambda:parameter_DOO(uName))
    b6 = tk.Button(window_pc, text='AOOR', state = 'disable',command=lambda:parameter_AOOR(uName))
    b7 = tk.Button(window_pc, text='VOOR', state = 'disable',command=lambda:parameter_VOOR(uName))
    b8 = tk.Button(window_pc, text='AAIR', state = 'disable',command=lambda:parameter_AAIR(uName))
    b9 = tk.Button(window_pc, text='VVIR', state = 'disable',command=lambda:parameter_VVIR(uName))
    b10 = tk.Button(window_pc, text='DOOR', state = 'disable',command=lambda:parameter_DOOR(uName))
    b11 = tk.Button(window_pc, text="Display user's info", command=lambda: verify(uName))
    b12 = tk.Button(window_pc, text='Show Egram', state = 'disable',command=lambda:showegram(uName))
    b13 = tk.Button(window_pc, text='Sign Out', command=sign_out)
    b1.grid(column=50, row=30)
    b2.grid(column=51, row=30)
    b3.grid(column=52, row=30)
    b4.grid(column=53, row=30)
    b5.grid(column=54, row=30)
    b6.grid(column=50, row=35)
    b7.grid(column=51, row=35)
    b8.grid(column=52, row=35)
    b9.grid(column=53, row=35)
    b10.grid(column=54, row=35)
    b11.grid(column=56, row=35)
    b12.grid(column=56, row=30)
    b13.grid(column=32, row=37)

    #switch button state when clicked connect and disconnect

    def connect_check(args):
        if "COM" in clicked_com.get() :
            connect_bt["state"] = "active"
            b1["state"] = "active"
            b2["state"] = "active"
            b3["state"] = "active"
            b4["state"] = "active"
            b5["state"] = "active"
            b6["state"] = "active"
            b7["state"] = "active"
            b8["state"] = "active"
            b9["state"] = "active"
            b10["state"] = "active"
            b11["state"] = "active"
            b12["state"] = "active"

        else:
            connect_bt["state"] = "disable"
            b1["state"] = "disable"
            b2["state"] = "disable"
            b3["state"] = "disable"
            b4["state"] = "disable"
            b5["state"] = "disable"
            b6["state"] = "disable"
            b7["state"] = "disable"
            b8["state"] = "disable"
            b9["state"] = "disable"
            b10["state"] = "disable"
            b11["state"] = "disable"
            b12["state"] = "disable"

    #global connexion
    #If the connect button shows as "Disconnect", enable all the button expext the drop-down port selection menu and refresh button. Vice versa.


#Sign out the current user, go back to the login window
def sign_out():
    window_pc.destroy()
    main_window()

#Detect ports
def checkConnect():
    try:
        ser = serial.Serial(port="COM6", baudrate=115200)
        return 6
    except:
        try:
            ser = serial.Serial(port="COM7", baudrate=115200)
            return 7
        except:
            return 0

#Check ports connection, return corresponding message
def connect():
    global ser
    global ports
    ports = list(list_ports.comports())
    ser = serial.Serial(port = "COM6",baudrate = 115200)
    if ser.is_open:
        messagebox.showinfo("System Message", "Connected")
        print(ser)
        ser.close()
    else:
        ser.close()
        messagebox.showerror("System Message", "Disconnected")

#Close port for next time
def disconnect():
    global ser
    ser.close()

#If the connect button shows as "Disconnect", enable all the button, vice versa
def connexion():
    global ser,serialData
    if connect_bt ["text"] in "Disconnect":
        serialData = False
        connect_bt["text"] ="Connect"
        refresh["state"] = "active"
        drop_COM["state"] = "active"
        disconnect()
    else:
        serialData = True
        connect_bt["text"] = "Disconnect"
        refresh["state"] = "disable"
        drop_COM["state"] = "disable"
        port = clicked_com.get()
        connect()

main_window()

