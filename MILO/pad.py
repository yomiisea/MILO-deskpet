from tkinter import *
from tkcalendar import Calendar


tkobj = Tk()



tkobj.geometry("400x400")
tkobj.title("Milo")
#creating a calender object

tkc = Calendar(tkobj,selectmode = "day",year=2022,month=1,date=1)


tkc.pack(pady=40)



def fetch_date():
    date.config(text = "La fecha es: " + tkc.get_date())



but = Button(tkobj,text="Elegir Fecha",command=fetch_date, bg="black", fg='white')

but.pack()

date = Label(tkobj,text="",bg='black',fg='white')
date.pack(pady=20)

tkobj.mainloop()