import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
import os

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def create_wav():
   filewin = Toplevel(root)

def open_data(e1):
    for element in os.listdir('.'):
       if element == e1.get():
          print("Le fichier %s existe \n" % (e1.get()))
          print("hEllO WOrlD")
       else:
          print("**\n")
   
def open_son():
   filewin = Toplevel(root)
   Label(filewin, text="Name").grid(row=0)
   e1 = Entry(filewin)
   e1.grid(row=0, column=1)
   Button(filewin, text='Quit', command=filewin.quit).grid(row=3, column=0, sticky=W, pady=4)
   opendata=open_data(e1)
   Button(filewin, text='Enter', command= opendata ).grid(row=3, column=1, sticky=W, pady=4)

   
root = tk.Tk()
menubar= Menu(root)

filemenu = Menu(menubar, tearoff = 0)

newmenu = Menu(menubar, tearoff = 0)
newmenu.add_command(label="New wav", command= create_wav)
filemenu.add_cascade(label="New", menu= newmenu)

filemenu.add_command(label="Open", command=open_son)

filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)


root.config(menu=menubar)
mainloop()
