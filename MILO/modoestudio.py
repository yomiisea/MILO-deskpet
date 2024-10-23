import time
import requests
from tkinter import *
from tkinter import messagebox
import tkinter as tk

estudio = ""
hour = ""
minute = ""
second = ""
temp=0

#estudio = Tk()

def doestudio(win,callback):
    global hour,minute,second,estudio
    estudio =Toplevel(win)
    estudio.geometry("410x300")
    estudio.title("MODO ESTUDIO")
    estudio.config(bg=('#53a384'))
    hour=StringVar()
    minute=StringVar()
    second=StringVar()
    hour.set(" 00")
    minute.set(" 00")
    second.set(" 00")
    titulo= Label(estudio, text="  Pongamonos a Trabajar!  ", relief="raised", fg="black", bg="#d4dd94", font=("Helevetica", 18, "bold")).place(x=53, y=20)
    especifico=Label(estudio, text="    H          M         S      ", relief="sunken", fg="white", bg="black", font=("Helevetica", 12, "bold")).place(x=126, y=120)
    hourEntry = Entry(estudio, width=3, font=("Arial", 18, ""),
                  textvariable=hour)
    hourEntry.place(x=132, y=80)

    minuteEntry = Entry(estudio, width=3, font=("Arial", 18, ""),
                    textvariable=minute)
    minuteEntry.place(x=182, y=80)

    secondEntry = Entry(estudio, width=3, font=("Arial", 18, ""),
                    textvariable=second)
    secondEntry.place(x=232, y=80)
    btn = Button(estudio, text='Empezar con el Estudio', bd='5',
                 command=lambda: submit(callback))
    btn.place(x=135, y=180)

def finestudio():
    global temp
    print("finestudio")
    temp=-10

def task1(callback):
    global temp
    mins, secs = divmod(temp, 60)
    hours = 0
    if mins > 60:
        hours, mins = divmod(mins, 60)
    hour.set("{0:2d}".format(hours))
    minute.set("{0:2d}".format(mins))
    second.set("{0:2d}".format(secs))
    estudio.update()
    sw=True
    if (temp <= 0):
        if (temp > -5):
            callback()
            messagebox.showinfo("MODO ESTUDIO", "TERMINO EL TIEMPO, BIEN HECHO!")
            response = requests.get("http://192.168.0.20/?alarma=10")
        else:
            messagebox.showinfo("MODO ESTUDIO", "ESTUDIO CANCELADO")
        estudio.destroy()
        estudio.update()
        sw=False
    temp -= 1
    if(sw):
        estudio.after(1000, lambda : task1(callback))

def submit(callback):
    global estudio,temp
    try:
        temp = int(hour.get()) * 3600 + int(minute.get()) * 60 + int(second.get())
    except:
        print("Por favor ingrese el valor correcto")
    btn = Button(estudio, text='Concluir con el Estudio', bd='5',
                 command=finestudio)
    btn.place(x=135, y=230)
    estudio.after(1000,lambda : task1(callback))
    '''
    while temp > -1:
        mins, secs = divmod(temp, 60)
        hours = 0
        if mins > 60:
            hours, mins = divmod(mins, 60)
        hour.set("{0:2d}".format(hours))
        minute.set("{0:2d}".format(mins))
        second.set("{0:2d}".format(secs))
        estudio.update()
        time.sleep(1)
        if (temp <= 0):
            if(temp>-5):
                callback()
                messagebox.showinfo("MODO ESTUDIO", "TERMINO EL TIEMPO, BIEN HECHO!")
            else:
                messagebox.showinfo("MODO ESTUDIO", "ESTUDIO CANCELADO")
            estudio.destroy()
            estudio.update()
        temp -= 1
    '''


# estudio.mainloop()