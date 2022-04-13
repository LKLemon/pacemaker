import tkinter as tk

def invaild_input():
    window_error = tk.Toplevel()
    window_error.geometry('350x100')
    window_error.title('Waring!')
    label = tk.Label(window_error, text = 'Invaild input, please enter vaild username and passord!')
    label.place(x=22,y=35)
    label.pack()
    window_error.mainloop()

def repeat_user():
    window_error = tk.Toplevel()
    window_error.geometry('250x100')
    window_error.title('Waring!')
    label = tk.Label(window_error, text = 'User existed.\n Please enter a differnet username.')
    label.place(x=22, y=35)
    label.pack()
    window_error.mainloop()


def success():
    window_error = tk.Toplevel()
    window_error.geometry('170x100')
    window_error.title('Success!')
    label =tk.Label(window_error, text='Suceess!')
    label.place(x=50, y=50)
    label.pack()
    window_error.mainloop()
