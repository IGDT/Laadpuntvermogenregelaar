#https://www.plus2net.com/python/tkinter-Toplevel-data.php
import tkinter as tk
from tkinter import *
from tkinter import ttk

root = tk.Tk()
root.geometry("300x300")
root.title("Laadpunt vermogen regelaar")

my_str = tk.StringVar()
IPentry = tk.Entry(root, textvariable=my_str)
IPentry.grid(row=0, column=1)
my_str.set("10.0.0.182")
# add one button
button4 = tk.Button(root, text='Keyboard', command=lambda: my_open())
button4.grid(row=2, column=2)

def my_open():
    global e1
    # label frame
    root_keyboard = Toplevel(root)  # Child window
    root_keyboard.geometry("300x300")  # Size of the window
    root_keyboard.title("Input")

    lfnumbers = LabelFrame(root_keyboard, text='Numbers')
    lfnumbers.grid(row=1, column=0)

    e1 = tk.Entry(root_keyboard, width=20)
    e1.grid(row=0, column=0)
    enterbutton = tk.Button(lfnumbers, text='Enter', command=lambda: my_str.set(e1.get()))
    enterbutton.grid(row=5, column=0, ipadx=6, ipady=10)
    closebutton = tk.Button(lfnumbers, text='Close', command=root_keyboard.destroy)
    closebutton.grid(row=5, column=1, ipadx=6, ipady=10)
    clearbutton = tk.Button(lfnumbers, text='Clear', command=lambda: e1.delete(0, END))
    clearbutton.grid(row=5, column=2, ipadx=6, ipady=10)

    # cijfers
    zeven = ttk.Button(lfnumbers, text='7', width=6, command=lambda: press('7'))
    zeven.grid(row=1, column=0, ipadx=6, ipady=10)

    acht = ttk.Button(lfnumbers, text='8', width=6, command=lambda: press('8'))
    acht.grid(row=1, column=1, ipadx=6, ipady=10)

    negen = ttk.Button(lfnumbers, text='9', width=6, command=lambda: press('9'))
    negen.grid(row=1, column=2, ipadx=6, ipady=10)

    # Second Line Button
    vier = ttk.Button(lfnumbers, text='4', width=6, command=lambda: press('4'))
    vier.grid(row=2, column=0, ipadx=6, ipady=10)

    vijf = ttk.Button(lfnumbers, text='5', width=6, command=lambda: press('5'))
    vijf.grid(row=2, column=1, ipadx=6, ipady=10)

    zes = ttk.Button(lfnumbers, text='6', width=6, command=lambda: press('6'))
    zes.grid(row=2, column=2, ipadx=6, ipady=10)

    # third line Button

    een = ttk.Button(lfnumbers, text='1', width=6, command=lambda: press('1'))
    een.grid(row=3, column=0, ipadx=6, ipady=10)

    twee = ttk.Button(lfnumbers, text='2', width=6, command=lambda: press('2'))
    twee.grid(row=3, column=1, ipadx=6, ipady=10)

    drie = ttk.Button(lfnumbers, text='3', width=6, command=lambda: press('3'))
    drie.grid(row=3, column=2, ipadx=6, ipady=10)

    # Fourth Line Button

    nul = ttk.Button(lfnumbers, text='0', width=6, command=lambda: press('0'))
    nul.grid(row=4, column=0, ipadx=6, ipady=10)

    dot = ttk.Button(lfnumbers, text='.', width=6, command=lambda: press('.'))
    dot.grid(row=4, column=1, ipadx=6, ipady=10)

def press(num):
    e1.insert(50, num)
root.mainloop()