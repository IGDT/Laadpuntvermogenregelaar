'''
Laadpaal regelen a.d.h.v. een popup scherm met verschillende opties.

Ontwikkelaar: Dillian Martens
In opdracht van Stagobel Electro

© Onder geen omstandigheden mag dit gekopieërd worden zonder toestemming van de ontwikkelaar.
'''

from tkinter import messagebox
from pyModbusTCP.client import ModbusClient
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Laadpunt vermogen regelaar')
root.geometry("600x300")

messagebox.showinfo("Info", "Programma gestart.")

statusEntry = Entry(root, width = 30)
statusEntry.grid(row = 1, column = 1)
statusEntry.config(state="disabled")
my_str = tk.StringVar()
my_str2 = tk.StringVar()
IPentry = tk.Entry(root, textvariable=my_str, width = 30)
IPentry.grid(row=2, column=1)
VermogenEntry = tk.Entry(root, textvariable=my_str2, width = 30)
VermogenEntry.grid(row=3, column=1)
my_str.set("10.0.0.182")
my_str2.set("20")

options = [
    "Kies een waarde",
    "6A",
    "8A",
    "10A",
    "16A",
]
clicked = StringVar()
clicked.set(options[0])

drop = OptionMenu(root, clicked, *options).grid(row = 1, column = 2)

workmode = 0

labelStatustekst = Label(root, text="Status: ")
labelStatustekst.grid(row = 1, column = 0)
labelIPtekst = Label(root, text="IP-adres: ")
labelIPtekst.grid(row = 2, column = 0)
labelVermogentekst = Label(root, text="Vermogen huis: ")
labelVermogentekst.grid(row = 3, column = 0)

lfstatus = LabelFrame(root, text='Laadstatus')
lfstatus.place(x=50, y=100)
lfbuttons = LabelFrame(root, text='Laadknoppen')
lfbuttons.place(x=50, y=150)

buttonAutomatisch = Button(lfbuttons, text="Automatisch", width = 15, height = 2, command=lambda *args: setWorkmode(1))
buttonAutomatisch.grid(row = 7, column = 0)
buttonZelf = Button(lfbuttons, text="Zelf instellen", width = 15, height = 2, command=lambda *args: setWorkmode(2))
buttonZelf.grid(row = 7, column = 1)
buttonStoppen = Button(lfbuttons, text="Stoppen met laden", width = 15, height = 2, command=lambda *args: setWorkmode(3))
buttonStoppen.grid(row = 7, column = 2)
buttonInstellingenIP = tk.Button(root, text='Instellingen', width = 8, command=lambda *args: my_open(4))
buttonInstellingenIP.grid(row=2, column=2)
buttonInstellingVermogen = tk.Button(root, text='Instellingen', width = 8, command=lambda *args: my_open(5))
buttonInstellingVermogen.grid(row=3, column=2)

my_progress = ttk.Progressbar(lfstatus, orient = HORIZONTAL, length = 490, mode = 'indeterminate')
my_progress.grid(row = 4, column = 1)

def setWorkmode(value):
    SERVER_HOST = IPentry.get()  # IP-adres van de laadpaal
    SERVER_PORT = 502  # Deze poort moet 502 zijn

    c = ModbusClient()

    c.host(SERVER_HOST)
    c.port(SERVER_PORT)

    global workmode
    workmode = value

    if not c.is_open():
        if not c.open():
            print("Unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))
            messagebox.showerror("Error!", "Kan niet verbinden met het opgegeven IP-adres.")
    if c.is_open():
        print("Connected to " + SERVER_HOST + ":" + str(SERVER_PORT))

        if workmode == 1:
            statusEntry.config(state="normal")
            statusEntry.delete(0, 'end')
            Labelautomatisch = Label(root, text=statusEntry.insert(1, "Automatisch laden ingeschakeld"))
            statusEntry.config(state="disabled")
            my_progress.stop()
            my_progress.start(10)
            os.system('python test.py')
        elif workmode == 2:
            if clicked.get() == "6A":
                print("6A")
                statusEntry.config(state="normal")
                statusEntry.delete(0, 'end')
                LabelZelfInstellen = Label(root, text=statusEntry.insert(1, "Laadstroom zelf ingesteld"))
                statusEntry.config(state="disabled")
                my_progress.stop()
                my_progress.start(20)
                regs = c.write_single_register(1000, 6)
            elif clicked.get() == "8A":
                print("8A")
                statusEntry.config(state="normal")
                statusEntry.delete(0, 'end')
                LabelZelfInstellen = Label(root, text=statusEntry.insert(1, "Laadstroom zelf ingesteld"))
                statusEntry.config(state="disabled")
                my_progress.stop()
                my_progress.start(15)
                regs = c.write_single_register(1000, 8)
            elif clicked.get() == "10A":
                print("10A")
                statusEntry.config(state="normal")
                statusEntry.delete(0, 'end')
                LabelZelfInstellen = Label(root, text=statusEntry.insert(1, "Laadstroom zelf ingesteld"))
                statusEntry.config(state="disabled")
                my_progress.stop()
                my_progress.start(10)
                regs = c.write_single_register(1000, 10)
            elif clicked.get() == "16A":
                print("16A")
                statusEntry.config(state="normal")
                statusEntry.delete(0, 'end')
                LabelZelfInstellen = Label(root, text=statusEntry.insert(1, "Laadstroom zelf ingesteld"))
                statusEntry.config(state="disabled")
                my_progress.stop()
                my_progress.start(5)
                regs = c.write_single_register(1000, 16)
            else:
                messagebox.showerror("Warning!", "Vergeet de maximale stroom niet te kiezen in de menu.")
        elif workmode == 3:
            statusEntry.config(state="normal")
            statusEntry.delete(0, 'end')
            LabelNietLaden = Label(root, text=statusEntry.insert(1, "Laadpunt niet aan het laden"))
            statusEntry.config(state="disabled")
            my_progress.stop()
            regs = c.write_single_register(1000, 0)
        else:
            print("error")

root.mainloop()