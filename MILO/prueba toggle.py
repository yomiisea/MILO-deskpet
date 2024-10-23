from tkinter import *
from tkinter import PhotoImage
import tkinter.messagebox

root = Tk()
root.title('MILO')
root.geometry('350x500')

bg = PhotoImage(file = 'milo2.png')
canvas1 = Canvas(root, width=350,
                 height=500)
canvas1.create_image( 0, 0, image = bg,
                     anchor = "nw")
canvas1.pack(fill="both", expand=True)


btn_state=False

nav_icon = PhotoImage(file='navbar.png')
close_icon = PhotoImage(file='close.png')
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

label = Label(root, font='ariel 18 bold')
label.place(x=60, y=250)

NavBar = Frame(root, bg='black', height=1000, width=250)
NavBar.place(x=-250, y=0)
def option_selected(msg):
    switch()
    label.config(text=msg)

option1 = Button(NavBar, text='Tareas', font='ariel 18 bold', bg='black', fg='white', activebackground='gray',
                 activeforeground='white', bd=0, command=lambda msg='TAREAS': option_selected(msg)).place(x=25, y=60)
option2 = Button(NavBar, text='Vida', font='ariel 18 bold', bg='black', fg='white', activebackground='gray',
                 activeforeground='white', bd=0, command=lambda msg='Mostrar Vida': option_selected(msg)).place(x=25, y=120)
option3 = Button(NavBar, text='Modo estudio', font='ariel 18 bold', bg='black', fg='white', activebackground='gray',
                 activeforeground='white', bd=0, command=lambda msg='Activar modo estudio': option_selected(msg)).place(x=25, y=180)
option4 = Button(NavBar, text='Playlist', font='ariel 18 bold', bg='black', fg='white', activebackground='gray',
                 activeforeground='white', bd=0, command=lambda msg='insertar playlist youtube': option_selected(msg)).place(x=25, y=240)
option5 = Button(NavBar, text='Horario', font='ariel 18 bold', bg='black', fg='white', activebackground='gray',
                 activeforeground='white', bd=0, command=lambda msg='Horario': option_selected(msg)).place(x=25, y=300)


close_btn = Button(NavBar, image=close_icon, bg='black', bd=0, command=switch)
close_btn.place(x=200, y=5)
root.mainloop()