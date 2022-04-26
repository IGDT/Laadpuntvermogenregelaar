'''
Laadpaal regelen a.d.h.v. een popup scherm met verschillende opties.

Ontwikkelaar: Dillian Martens
In opdracht van Stagobel Electro

© Onder geen omstandigheden mag dit gekopieërd worden zonder toestemming van de ontwikkelaar.
'''

from tkinter import messagebox
from pyModbusTCP.client import ModbusClient
import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import serial
import time
import os
import sys
from PIL import Image
from PIL import ImageTk

root = Tk()
root.title('Laadpunt vermogen regelaar')
root.geometry("750x500")

messagebox.showinfo("Info", "Programma gestart.")

statusEntry = Entry(root, width = 30)
statusEntry.grid(row = 1, column = 1)
statusEntry.config(state="disabled")
stroomEntry = Entry(root, width = 15)
stroomEntry.grid(row = 1, column = 2)
stroomEntry.config(state="disabled")
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

drop = OptionMenu(root, clicked, *options).grid(row = 4, column = 1)

workmode = 0

ser = serial.Serial()

ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE

ser.xonxoff = 0
ser.rtscts = 0
ser.timeout = 12
ser.port = "/dev/ttyUSB0"
ser.close()

injectieWatt = 0
afnameWatt = 0
overschotafname = 0
overschotinjectie = 0

SERVER_HOST = IPentry.get()
SERVER_PORT = 502  # Deze poort moet 502 zijn

c = ModbusClient()

c.host(SERVER_HOST)
c.port(SERVER_PORT)

def uitlezen():
    global afnameWatt
    global injectieWatt
    while True:
        ser.open()
        checksum_found = False
        if not c.is_open():
            if not c.open():
                print("Unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))
        if c.is_open():
            print("Connected to " + SERVER_HOST + ":" + str(SERVER_PORT))

            while not checksum_found:
                telegram_line = ser.readline()
                telegram_line = telegram_line.decode('ascii').strip()
                huishoudelijkvermogen = int(VermogenEntry.get())  # 230V x 40A = 9200W

                if telegram_line[0:9] == "1-0:1.7.0":
                    afnameKw = telegram_line[10:15]
                    afnameWatt = float(afnameKw) * 1000
                    afnameWatt = int(afnameWatt)

                    if workmode == 1:
                        if afnameWatt > 0:
                            overschotafname = huishoudelijkvermogen - afnameWatt
                            print(overschotafname)
                            if 1 <= overschotafname <= 20:
                                regs = c.write_single_register(1000, 6)
                                my_progress.stop()
                                my_progress.start(20)
                                stroomEntry.config(state="normal")
                                stroomEntry.delete(0, 'end')
                                Labelstroom = Label(root, text=stroomEntry.insert(1, "6A afname"))
                                stroomEntry.config(state="disabled")
                                if regs:
                                    print("laadpaal sturen naar 6A afname:", regs)
                            elif 21 <= overschotafname <= 30:
                                regs = c.write_single_register(1000, 8)
                                my_progress.stop()
                                my_progress.start(15)
                                stroomEntry.config(state="normal")
                                stroomEntry.delete(0, 'end')
                                Labelstroom = Label(root, text=stroomEntry.insert(1, "8A afname"))
                                stroomEntry.config(state="disabled")
                                if regs:
                                    print("laadpaal sturen naar 8A afname:", regs)
                            elif 31 <= overschotafname <= 40:
                                regs = c.write_single_register(1000, 10)
                                my_progress.stop()
                                my_progress.start(10)
                                stroomEntry.config(state="normal")
                                stroomEntry.delete(0, 'end')
                                Labelstroom = Label(root, text=stroomEntry.insert(1, "10A afname"))
                                stroomEntry.config(state="disabled")
                                if regs:
                                    print("laadpaal sturen naar 10A afname:", regs)
                            elif overschotafname > 41:
                                regs = c.write_single_register(1000, 16)
                                my_progress.stop()
                                my_progress.start(5)
                                stroomEntry.config(state="normal")
                                stroomEntry.delete(0, 'end')
                                Labelstroom = Label(root, text=stroomEntry.insert(1, "16A afname"))
                                stroomEntry.config(state="disabled")
                                if regs:
                                    print("laadpaal sturen naar 16A afname:", regs)
                            else:
                                print("Te weinig vermogen om te laden.")
                                stroomEntry.config(state="normal")
                                stroomEntry.delete(0, 'end')
                                Labelstroom = Label(root, text=stroomEntry.insert(1, "Te weinig vermogen"))
                                stroomEntry.config(state="disabled")
                                my_progress.stop()
                                regs = c.write_single_register(1000, 0)

                if telegram_line[0:9] == "1-0:2.7.0":
                    injectieKw = telegram_line[10:15]
                    injectieWatt = float(injectieKw) * 1000
                    injectieWatt = int(injectieWatt)

                    if workmode == 1:
                        if injectieWatt > 0:
                            overschotinjectie = huishoudelijkvermogen - injectieWatt
                            print(overschotinjectie)
                            if overschotinjectie < 0:
                                if -5 >= overschotinjectie >= -20:
                                    regs = c.write_single_register(1000, 6)
                                    my_progress.stop()
                                    my_progress.start(20)
                                    stroomEntry.config(state="normal")
                                    stroomEntry.delete(0, 'end')
                                    Labelstroom = Label(root, text=stroomEntry.insert(1, "6A injectie"))
                                    stroomEntry.config(state="disabled")
                                    if regs:
                                        print("laadpaal sturen naar 6A injectie:", regs)
                                elif -21 >= overschotinjectie >= -30:
                                    regs = c.write_single_register(1000, 8)
                                    my_progress.stop()
                                    my_progress.start(15)
                                    stroomEntry.config(state="normal")
                                    stroomEntry.delete(0, 'end')
                                    Labelstroom = Label(root, text=stroomEntry.insert(1, "8A injectie"))
                                    stroomEntry.config(state="disabled")
                                    if regs:
                                        print("laadpaal sturen naar 8A injectie:", regs)
                                elif -31 >= overschotinjectie >= -40:
                                    regs = c.write_single_register(1000, 10)
                                    my_progress.stop()
                                    my_progress.start(10)
                                    stroomEntry.config(state="normal")
                                    stroomEntry.delete(0, 'end')
                                    Labelstroom = Label(root, text=stroomEntry.insert(1, "10A injectie"))
                                    stroomEntry.config(state="disabled")
                                    if regs:
                                        print("laadpaal sturen naar 10A injectie:", regs)
                                elif overschotinjectie > -41:
                                    regs = c.write_single_register(1000, 16)
                                    my_progress.stop()
                                    my_progress.start(5)
                                    stroomEntry.config(state="normal")
                                    stroomEntry.delete(0, 'end')
                                    Labelstroom = Label(root, text=stroomEntry.insert(1, "16A injectie"))
                                    stroomEntry.config(state="disabled")
                                    if regs:
                                        print("laadpaal sturen naar 16A injectie:", regs)
                                else:
                                    print("Te weinig vermogen om te laden.")
                                    my_progress.stop()
                                    regs = c.write_single_register(1000, 0)
                            else:
                                print("Meer verbruik dan injectie dus niet laden.")
                                stroomEntry.config(state="normal")
                                stroomEntry.delete(0, 'end')
                                Labelstroom = Label(root, text=stroomEntry.insert(1, "Te veel verbruik"))
                                stroomEntry.config(state="disabled")
                                my_progress.stop()
                                regs = c.write_single_register(1000, 0)
        ser.close()

def datatonen():
    while True:
        LabelAfname = Label(lfdata, text="Afname: " + str(afnameWatt) + "W")
        LabelAfname.grid(row=0, column=0)
        LabelInjectie = Label(lfdata, text="Injectie: "+ str(injectieWatt) + "W")
        LabelInjectie.grid(row=1, column=0)
        time.sleep(1)
        LabelInjectie.destroy()
        LabelAfname.destroy()

def setWorkmode(value):
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
            Labelautomatisch = Label(root, text=statusEntry.insert(1, "Automatisch laden"))
            statusEntry.config(state="disabled")

        elif workmode == 2:
            if clicked.get() == "6A":
                print("6A")
                statusEntry.config(state="normal")
                statusEntry.delete(0, 'end')
                LabelZelfInstellen = Label(root, text=statusEntry.insert(1, "Laadstroom zelf ingesteld"))
                statusEntry.config(state="disabled")
                my_progress.stop()
                my_progress.start(20)
                stroomEntry.config(state="normal")
                stroomEntry.delete(0, 'end')
                Labelstroom = Label(root, text=stroomEntry.insert(1, "6A zelf"))
                stroomEntry.config(state="disabled")
                regs = c.write_single_register(1000, 6)
            elif clicked.get() == "8A":
                print("8A")
                statusEntry.config(state="normal")
                statusEntry.delete(0, 'end')
                LabelZelfInstellen = Label(root, text=statusEntry.insert(1, "Laadstroom zelf ingesteld"))
                statusEntry.config(state="disabled")
                my_progress.stop()
                my_progress.start(15)
                stroomEntry.config(state="normal")
                stroomEntry.delete(0, 'end')
                Labelstroom = Label(root, text=stroomEntry.insert(1, "8A zelf"))
                stroomEntry.config(state="disabled")
                regs = c.write_single_register(1000, 8)
            elif clicked.get() == "10A":
                print("10A")
                statusEntry.config(state="normal")
                statusEntry.delete(0, 'end')
                LabelZelfInstellen = Label(root, text=statusEntry.insert(1, "Laadstroom zelf ingesteld"))
                statusEntry.config(state="disabled")
                my_progress.stop()
                my_progress.start(10)
                stroomEntry.config(state="normal")
                stroomEntry.delete(0, 'end')
                Labelstroom = Label(root, text=stroomEntry.insert(1, "10A zelf"))
                stroomEntry.config(state="disabled")
                regs = c.write_single_register(1000, 10)
            elif clicked.get() == "16A":
                print("16A")
                statusEntry.config(state="normal")
                statusEntry.delete(0, 'end')
                LabelZelfInstellen = Label(root, text=statusEntry.insert(1, "Laadstroom zelf ingesteld"))
                statusEntry.config(state="disabled")
                my_progress.stop()
                my_progress.start(5)
                stroomEntry.config(state="normal")
                stroomEntry.delete(0, 'end')
                Labelstroom = Label(root, text=stroomEntry.insert(1, "16A zelf"))
                stroomEntry.config(state="disabled")
                regs = c.write_single_register(1000, 16)
            else:
                messagebox.showerror("Warning!", "Vergeet de maximale stroom niet te kiezen in de menu.")
        elif workmode == 3:
            statusEntry.config(state="normal")
            statusEntry.delete(0, 'end')
            LabelNietLaden = Label(root, text=statusEntry.insert(1, "Laadpunt niet aan het laden"))
            statusEntry.config(state="disabled")
            my_progress.stop()
            stroomEntry.config(state="normal")
            stroomEntry.delete(0, 'end')
            Labelstroom = Label(root, text=stroomEntry.insert(1, ""))
            stroomEntry.config(state="disabled")
            regs = c.write_single_register(1000, 0)
        else:
            print("Error in work modes.")

def my_open(mode):
    global keuze
    keuze = mode
    global KeyboardEntry

    root_keyboard = Toplevel(root)
    root_keyboard.geometry("250x300")

    lfnumbers = LabelFrame(root_keyboard, text='Input')
    lfnumbers.grid(row=1, column=0)

    if keuze == 4:
        messagebox.showwarning("Warning!", "Het is aangeraden dat alleen de installateurs dit aanpassen!")
        root_keyboard.title("IP-adres")
        enterbutton = tk.Button(lfnumbers, text='Enter', command=lambda: my_str.set(KeyboardEntry.get()) and KeyboardEntry.delete(0, END))
        enterbutton.grid(row=5, column=0, ipadx=6, ipady=10)
        dot = ttk.Button(lfnumbers, text='.', width=6, command=lambda: press('.'))
        dot.grid(row=4, column=2, ipadx=6, ipady=10)
    elif keuze == 5:
        messagebox.showwarning("Warning!", "Het is aangeraden dat alleen de installateurs dit aanpassen!")
        root_keyboard.title("Vermogen")
        enterbutton = tk.Button(lfnumbers, text='Enter', command=lambda: my_str2.set(KeyboardEntry.get()) and KeyboardEntry.delete(0, END))
        enterbutton.grid(row=5, column=0, ipadx=6, ipady=10)
    else:
        messagebox.showerror("Warning!", "Error in keyboard menu.")

    KeyboardEntry = tk.Entry(root_keyboard, width=20)
    KeyboardEntry.grid(row=0, column=0)

    closebutton = tk.Button(lfnumbers, text='Close', command=root_keyboard.destroy)
    closebutton.grid(row=5, column=1, ipadx=6, ipady=10)
    clearbutton = tk.Button(lfnumbers, text='Clear', command=lambda: KeyboardEntry.delete(0, END))
    clearbutton.grid(row=5, column=2, ipadx=6, ipady=10)

    zeven = ttk.Button(lfnumbers, text='7', width=6, command=lambda: press('7'))
    zeven.grid(row=1, column=0, ipadx=6, ipady=10)

    acht = ttk.Button(lfnumbers, text='8', width=6, command=lambda: press('8'))
    acht.grid(row=1, column=1, ipadx=6, ipady=10)

    negen = ttk.Button(lfnumbers, text='9', width=6, command=lambda: press('9'))
    negen.grid(row=1, column=2, ipadx=6, ipady=10)

    vier = ttk.Button(lfnumbers, text='4', width=6, command=lambda: press('4'))
    vier.grid(row=2, column=0, ipadx=6, ipady=10)

    vijf = ttk.Button(lfnumbers, text='5', width=6, command=lambda: press('5'))
    vijf.grid(row=2, column=1, ipadx=6, ipady=10)

    zes = ttk.Button(lfnumbers, text='6', width=6, command=lambda: press('6'))
    zes.grid(row=2, column=2, ipadx=6, ipady=10)

    een = ttk.Button(lfnumbers, text='1', width=6, command=lambda: press('1'))
    een.grid(row=3, column=0, ipadx=6, ipady=10)

    twee = ttk.Button(lfnumbers, text='2', width=6, command=lambda: press('2'))
    twee.grid(row=3, column=1, ipadx=6, ipady=10)

    drie = ttk.Button(lfnumbers, text='3', width=6, command=lambda: press('3'))
    drie.grid(row=3, column=2, ipadx=6, ipady=10)

    nul = ttk.Button(lfnumbers, text='0', width=6, command=lambda: press('0'))
    nul.grid(row=4, column=1, ipadx=6, ipady=10)

def press(num):
    KeyboardEntry.insert(50, num)

def reboot():
    os.execl(sys.executable, sys.executable, *sys.argv)

labelStatustekst = Label(root, text="Status: ")
labelStatustekst.grid(row = 1, column = 0)
labelIPtekst = Label(root, text="IP-adres: ")
labelIPtekst.grid(row = 2, column = 0)
labelVermogentekst = Label(root, text="Vermogen: ")
labelVermogentekst.grid(row = 3, column = 0)
labelKeuze = Label(root, text="Keuze stroom:")
labelKeuze.grid(row = 4, column = 0)

width = 500
height = 100
img = Image.open("//home//pi//Downloads//stagobel_logo_transparant.png")
img = img.resize((width, height), Image.ANTIALIAS)
photoImg = ImageTk.PhotoImage(img)
label = Label(root, image=photoImg, width=500)
label.grid(row = 0, column = 1)

lfstatus = LabelFrame(root, text='Laadstatus')
lfstatus.place(x=100, y=250)
lfbuttons = LabelFrame(root, text='Laadknoppen')
lfbuttons.place(x=100, y=300)
lfdata = LabelFrame(root, text='Data digitale meter', padx=200)
lfdata.place(x=100, y=380)

my_progress = ttk.Progressbar(lfstatus, orient = HORIZONTAL, length = 490, mode = 'indeterminate')
my_progress.grid(row = 5, column = 1)

threading.Thread(target=uitlezen).start()
threading.Thread(target=datatonen).start()

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
buttonReboot = tk.Button(root, text="Reboot", width = 5, command=reboot, bg='red')
buttonReboot.grid(row = 0, column = 0)

root.mainloop()