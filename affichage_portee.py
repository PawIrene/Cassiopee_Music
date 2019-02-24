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

w1 = tk.Label(root, text= texte) #le label est un "enfant" de root, on précise le contenu du texte
w1.pack() #la méthode pack indique la taille de la fenêtre
w2 = tk.Label(root, compound = tk.CENTER, image=portee).pack(side="right")
w3 = tk.Label(root, compound = tk.RIGHT, image=note).pack(side="left")

#bout de code sensé afficher la portée en arrière plan avec Canvas
#top=Tk()

#C = Canvas(top, bg="blue", height=250, width=300)
#filename = PhotoImage(file = "portee.png")
#background_label = Label(top, image=portee)
#background_label.place(x=0, y=0, relwidth=1, relheight=1)

#C.pack()


mainloop()
#la fenêtre n'apparaît pas sans cette commande
