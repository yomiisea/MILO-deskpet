from os import path
from os.path import expanduser
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry

def newTask():
    global my_entry,sel,boxhora,lista,itemslista
    task = my_entry.get()
    fecha=sel.get()
    hora=boxhora.get()
    if task != "" and hora != "" and fecha != "":
        lista.insert(END, task+";"+fecha+";"+hora)
        my_entry.delete(0, "end")
    else:
        messagebox.showwarning("AVISO", "Ingrese alguna Tarea")

def deleteTask():
    lista.delete(ANCHOR)

def endTask():
    lista.delete(ANCHOR)

def tareas(win,callcambia,callcompleta,tlist = []):
    global my_entry,sel,boxhora,lista,itemslista
    a = Toplevel(win)
    a.title('TAREAS MILO')
    a.config(bg='#cb997e')
    a.geometry('600x550+600+300')
    a.resizable(width=False, height=False)
    cuadro = Frame(a)
    cuadro.pack(pady=8)
    task_list = tlist
    itemslista = StringVar(value=task_list)
    lista = Listbox(
        cuadro,
        width=35, height=8, font=('Times', 20), bd=0, fg='#0b132b',
        highlightthickness=0,
        selectbackground='#c1c1c1',
        activestyle="none",
        listvariable=itemslista
    )
    lista.pack(side=LEFT, fill=BOTH)


    sb = Scrollbar(cuadro)
    sb.pack(side=RIGHT, fill=BOTH)

    lista.config(yscrollcommand=sb.set)
    sb.config(command=lista.yview)

    cuadro_text = Frame(a)
    cuadro_text.pack(pady=1,fill='x',padx=20)

    labelText = StringVar()
    labelText.set("Tarea")
    labelDir = Label(cuadro_text, textvariable=labelText, height=1)
    labelDir.pack(fill=BOTH, expand=True, side=LEFT)
    my_entry = Entry(
        cuadro_text,
        font=('times', 23)
    )

    my_entry.pack(fill=BOTH, expand=True, side=LEFT)

    cuadro_fecha = Frame(a)
    cuadro_fecha.pack(pady=5)
    labelText1 = StringVar()
    labelText1.set("Fecha fin")
    labelDir1 = Label(cuadro_fecha, textvariable=labelText1, height=1)
    labelDir1.pack(fill=BOTH, expand=True, side=LEFT)

    sel = StringVar()
    cal = DateEntry(cuadro_fecha, selectmode='day', textvariable=sel,date_pattern='dd/MM/yyyy')
    cal.pack(fill=BOTH, expand=True, side=LEFT)

    labelText2 = StringVar()
    labelText2.set("Hora Fin (HH:MM)")
    labelDir2 = Label(cuadro_fecha, textvariable=labelText2, height=1)
    labelDir2.pack(fill=BOTH, expand=True, side=LEFT)
    boxhora = Entry(cuadro_fecha,font=('times', 12),width=5)
    boxhora.pack(fill=BOTH, expand=True, side=LEFT)

    boton_cuadro = Frame(a)
    boton_cuadro.pack(pady=18)

    addTask_btn = Button(
        boton_cuadro,
        font=('calibri 14'), bg='#ecc8af', text='Añadir Tarea',
        padx=30,
        pady=18,
        command=lambda : [newTask(), callcambia(lista.get(0, END))]
    )
    addTask_btn.pack(fill=BOTH, expand=True, side=LEFT)

    addTask_btn = Button(
        boton_cuadro,
        font=('calibri 14'), text='Tarea Completada', bg='#e7ad99',
        padx=30,
        pady=18,
        command=lambda: [deleteTask(), callcambia(lista.get(0, END)), callcompleta()]
    )

    addTask_btn.pack(fill=BOTH, expand=True, side=LEFT)

    delTask_btn = Button(
        boton_cuadro,
        font=('calibri 14'), text='Borrar Tarea', bg='#ce796b',
        padx=30,
        pady=10,
        command=lambda: [deleteTask(), callcambia(lista.get(0, END))]
    )
    delTask_btn.pack(fill=BOTH, expand=True, side=LEFT)
    #for item in task_list:
    #    lista.insert(END, item)


