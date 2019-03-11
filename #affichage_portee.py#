import tkinter as tk
#importe la bibliothèque tkinter permettant d'ouvrir des fenêtres
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox

root= tk.Tk() #création de la racine tk ie la fenêtre avec un titre
#ça doit être la première chose à écrire

portee = tk.PhotoImage(file="portee.png")
note = tk.PhotoImage(file="note_taille.png")
texte = "Application musicale en Python"
cle_de_sol = tk.PhotoImage(file="cle_de_sol.png")

w1 = tk.Label(root, text= texte) #le label est un "enfant" de root, on précise le contenu du texte
w1.pack() #la méthode pack indique la taille de la fenêtre
#w2 = tk.Label(root, compound = tk.CENTER, image=portee).pack(side="right")
#w3 = tk.Label(root, compound = tk.RIGHT, image=note).pack(side="left")


#------------------------------------------------------------------
canvas = Canvas(width = 500, height = 500, bg = 'white')
canvas.pack(expand = YES, fill = BOTH)

#bout de code fonctionnant:
#image = ImageTk.PhotoImage(file = "portee.png")
#canvas.create_image(10, 10, image = image, anchor = NW)

#création de la portée
for i in range(6):
    canvas.create_line(0, 50 * i, 400, 50 * i)
#canvas.create_line(50, 100, 250, 200, fill="red", width=10)
canvas.create_image(0,0, image=cle_de_sol, anchor=NW)

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

canvas.create_circle(200, 200, 25, fill="black")

mainloop()
#la fenêtre n'apparaît pas sans cette commande
