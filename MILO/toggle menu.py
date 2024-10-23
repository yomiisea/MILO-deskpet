from tkinter import *
from tkinter import PhotoImage
import requests
from datetime import datetime
from modoestudio import *
from modotareas import *

root = Tk()
root.title('MILO')
root.geometry('350x500')

vidas=5

taskList=[]

bg = PhotoImage(file = 'milo2.png')
canvas1 = Canvas(root, width=350,
                 height=500)
canvas1.create_image( 0, 0, image = bg,
                     anchor = "nw")
canvas1.pack(fill="both", expand=True)


btn_state=False

nav_icon = PhotoImage(file='navbar.png')
close_icon = PhotoImage(file='close.png')


def updateVida():
    global vidas
    response = requests.get("http://192.168.0.20/?vidas="+str(vidas))
    with open(expanduser('~/Documents/milovidas.csv'), 'w') as fp:
        fp.write(str(vidas))

def cargaVida():
    global vidas
    if path.exists(expanduser('~/Documents/milovidas.csv')):
        with open(expanduser('~/Documents/milovidas.csv'), 'r') as fp:
            stri=fp.readline()
        vidas=int(stri)
        response = requests.get("http://192.168.0.20/?vidas=" + str(vidas))

def loadtasks():
    global taskList
    print("load")
    if path.exists(expanduser('~/Documents/milotareas.csv')):
        with open(expanduser('~/Documents/milotareas.csv')) as file:
            taskList = file.readlines()
            taskList = [line.rstrip() for line in taskList]

def updateTasks(taskl):
    global taskList
    print("update")
    taskList=taskl
    with open(expanduser('~/Documents/milotareas.csv'), 'w') as fp:
        for item in taskList:
            fp.write("%s\n" % item)
            print(item)

def completaTask():
    global vidas
    print("completa")
    vidas=vidas+1
    updateVida()
    muestravidas()

def switch():
    global btn_state
    if btn_state is True:
        # close NavBar
        for x in range(251):
            NavBar.place(x=-x, y=0)
            frame.update()
        frame.config(bg="#7c6e62")
        # set button state off
        btn_state = False
    else:
        # Open NavBar
        for x in range(-250, 0):
            NavBar.place(x=x, y=0)
            frame.update()
        frame.config(bg="#7c6e62")
        # set button state ON
        btn_state = True

frame = Frame(canvas1, bg="#7c6e62")
frame.pack(side='top', fill=X)

navbar_btn = Button(frame, image=nav_icon, bg="#7c6e62", bd=0, command=switch)
navbar_btn.grid(row=1, column=1)

label = Label(root, font='ariel 18 bold', fg='#f00')
label.place(x=1, y=35)

NavBar = Frame(root, bg='black', height=1000, width=250)
NavBar.place(x=-250, y=0)

def muestravidas():
    global vidas
    str=''
    if(vidas<0):
        vidas=0
    if(vidas>8):
        vidas=8
    for i in range(vidas):
        str=str+'\u2764'
    label.config(text=str)

option1 = Button(NavBar, text='Tareas', font='ariel 18 bold', bg='black', fg='white', activebackground='gray',
                 activeforeground='white', bd=0, command=lambda : [tareas(root, updateTasks, completaTask, taskList),switch()]).place(x=25, y=60)
#option2 = Button(NavBar, text='Vida', font='ariel 18 bold', bg='black', fg='white', activebackground='gray',
#                 activeforeground='white', bd=0, command=lambda : [muestravidas(),switch()]).place(x=25, y=120)
option3 = Button(NavBar, text='Modo estudio', font='ariel 18 bold', bg='black', fg='white', activebackground='gray',
                 activeforeground='white', bd=0, command=lambda : [doestudio(root,completaTask),switch()]).place(x=25, y=180)

close_btn = Button(NavBar, image=close_icon, bg='black', bd=0, command=switch)
close_btn.place(x=200, y=5)
loadtasks()
cargaVida()
muestravidas()

def task():
    global vidas,taskList
    present=datetime.now()
    ntask=[]
    sw=False
    for item in taskList:
        t=item.split(';')
        datestr=t[1]+' '+t[2]+':00'
        date_time_obj = datetime.strptime(datestr, '%d/%m/%Y %H:%M:%S')
        if(present>date_time_obj):
            vidas=vidas-1
            updateVida()
            muestravidas()
            messagebox.showwarning('Milo', "Tarea "+t[0]+" vencida, pierdes una vida")
            sw=True
        else:
            ntask.append(item)
    if(sw):
        updateTasks(ntask)
    root.after(2000, task)  # reschedule event in 2 seconds

root.after(2000, task)
root.mainloop()