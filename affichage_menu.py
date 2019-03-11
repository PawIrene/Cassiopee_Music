import tkinter as tk
#importe la bibliothèque tkinter permettant d'ouvrir des fenêtres
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox

def affiche_portee():
    portee = tk.PhotoImage(file="portee.png")
    w1=tk.Label(root, compound = tk.CENTER, image=portee).pack(side="right")
    w1.pack()

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

root = tk.Tk()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

porteemenu=Menu(menubar, tearoff=0)
porteemenu.add_command(label="Nouvelle portee", command=affiche_portee)
menubar.add_cascade(label="Portee", menu=porteemenu)
"""
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)

editmenu.add_separator()

editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)

menubar.add_cascade(label="Edit", menu=editmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)
"""
root.config(menu=menubar)
root.mainloop()
