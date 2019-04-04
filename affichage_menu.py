import tkinter as tk
#importe la bibliothèque tkinter permettant d'ouvrir des fenêtres
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox

def affiche_note():

    note = tk.PhotoImage(file="Src/note_taille.png")
    canvas.pack(expand=YES, fill=BOTH)
    def _create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
    tk.Canvas.create_circle = _create_circle
    canvas.create_circle(200, 200, 25, fill="black")
    canvas.create_image(10,10,image=note, anchor=NW)
    """
    w2=tk.Label(root, compound = tk.LEFT, image=note).pack(side="left")
    w2.pack()
    """

def affiche_portee():
    cle_de_sol = tk.PhotoImage(file="Src/cle_de_sol.png")    
    canvas.pack(expand=YES, fill =BOTH)
    for i in range(6):
        canvas.create_line(0,50*i,400,50*i)
    canvas.create_image(0,0, image=cle_de_sol, anchor=NW)
    """ 
    BOUT DE CODE FONCTIONNANT MAIS PAS EN ARRIERE PLAN

    portee = tk.PhotoImage(file="portee.png")
    w1=tk.Label(root, compound = tk.CENTER, image=portee).pack(side="right")
    w1.pack()
    """

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

root = tk.Tk()
canvas = Canvas(width=500, height = 500, bg='white')
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
porteemenu.add_command(label="Ajouter note", command=affiche_note)
menubar.add_cascade(label="Portee", menu=porteemenu)

"""
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)

editmenu.add_separator()

editmenu.add_command(label="Ajouter Note", command=affiche_note)
menubar.add_cascade(label="Edit", menu=editmenu)

editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)


helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)
"""
root.config(menu=menubar)
mainloop()
