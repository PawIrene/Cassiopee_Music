import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
import os
import son
import shepard
import matplotlib.pyplot as plt

def create_shepard():
   donnee = shepard.noteShepard(13)
   donnee.graphFFT(fmax = 7500)
   plt.show()
   donnee.ecrire("noteShepard")

def inversion_spectre():
   donnee = son.ouvrir("la")
   donnee.graphFFT()
   donnee.inverseFFT()
   donnee.graphFFT()
   plt.show()
   donnee.decalFFT(-19000, [19100,22050])
   donnee.graphFFT()
   plt.show()
   donnee.ecrire("cassiopeReverse")

def grapheFFT(e1):
   donnee = shepard.note(int(e1))
   donnee.graphFFT()
   plt.show()

def decalFFT(e1):
   donnee = shepard.note(int(e1))
   donnee.decalFFT(-19000, [19100,22050])
   donnee.graphFFT()
   plt.show()
   
def add_some_action(e1):
   filewin = Toplevel(root)
   TEXTE = "Vous venez de créer un fichier son. Si vous souhaitez visualiser le module de la transformée de fourier, cliquez sur le boutton ci-dessous:"
   Label(filewin, text = TEXTE).grid(row=0)
   Button(filewin, text='Afficher le graphe FFT', command= lambda : grapheFFT(e1)).grid(row=1, column=1, sticky=W, pady=4)
   TEXTE2 = "Si vous souhaitez décaler la plage de fréquence, veuillez cliquer sur le boutton ci dessous."
   Label(filewin, text = TEXTE2).grid(row=2)
   Button(filewin, text='Inverser le graphe FFT', command= lambda : decalFFT(e1)).grid(row=3, column=1, sticky=W, pady=4)
   Button(filewin, text='Quit', command=filewin.quit).grid(row=3, column=0, sticky=W, pady=4)  

def create_son(e1):
   donnee = shepard.note(int(e1))   
   print("Création de la note de fréquence fondamentale", int(e1))
   add_some_action(e1)

def create_son_shepard(e1):
   donnee = shepard.noteShepard(int(e1))
   print("Creation de la note de Shepard de fréquence fondamentale", int(e1))
   add_some_action(e1)

def create_note_shepard():
   filewin = Toplevel(root)
   TEXTE = "Le nombre d'octet est fixé à 2. La durée est fixée à 3 secondes et le volume est à 0.5."
   Label(filewin, text = TEXTE).grid(row=0)
   Label(filewin, text="Fréquence fondamentale de la note (Hz) : ").grid(row=1)
   e1 = Entry(filewin)
   e1.grid(row=1, column=1)  
   Button(filewin, text='Créer la note de Shepard', command= lambda : create_son_shepard(e1.get())).grid(row=3, column=1, sticky=W, pady=4)
   Button(filewin, text='Quit', command=filewin.quit).grid(row=3, column=0, sticky=W, pady=4)   
   
def create_note():
   filewin = Toplevel(root)
   TEXTE = "Le nombre d'octet est fixé à 2 et la fréquence d'échantillonnage est déjà fixée à 44 100 Hz. La durée est fixée à 3 secondes et le volume est à 0.5."
   Label(filewin, text = TEXTE).grid(row=0)
   Label(filewin, text="Fréquence fondamentale de la note (Hz) : ").grid(row=1)
   e1 = Entry(filewin)
   e1.grid(row=1, column=1)  
   Button(filewin, text='Créer le son', command= lambda : create_son(e1.get())).grid(row=3, column=1, sticky=W, pady=4)
   Button(filewin, text='Quit', command=filewin.quit).grid(row=3, column=0, sticky=W, pady=4)
   
def open_data(e1):
   var = son.ouvrir(e1)
   print(var.fech)
   """
    for element in os.listdir('.'):
       if element == e1.get():
          print("Le fichier %s existe \n" % (e1.get()))
          print("hEllO WOrlD")
       else:
          print("**\n")
   """
def open_son():
   filewin = Toplevel(root)
   Label(filewin, text="Nom du fichier .wav").grid(row=0)
   e1 = Entry(filewin)
   e1.grid(row=0, column=1)
   
   Button(filewin, text='Quitter', command=filewin.quit).grid(row=3, column=0, sticky=W, pady=4)
   Button(filewin, text='Ouvrir le fichier', command= open_data(e1.get()) ).grid(row=3, column=1, sticky=W, pady=4)
   
root = tk.Tk()

ecran_accueil = Canvas(root, width=500, height=500, bg = "white")

photo = PhotoImage(file='Bienvenue2.png')
item = ecran_accueil.create_image(250,250, image=photo)
ecran_accueil.pack()

TEXTE2 = "Pour créer un fichier son, veuillez cliquer sur Fichier puis Nouveau."
TEXTE3 = "Pour ouvrir un fichier son déjà existant, veuillez cliquer sur Fichier puis Ouvrir."

label2 = tk.Label(root, text = TEXTE2, wraplength = 500, justify = tk.CENTER)
label2.pack()
label3 = tk.Label(root, text = TEXTE3, wraplength = 500, justify = tk.CENTER)
label3.pack()

menubar= Menu(root)

filemenu = Menu(menubar, tearoff = 0)

newmenu = Menu(menubar, tearoff = 0)
newmenu.add_command(label="Note", command=create_note)
newmenu.add_command(label="Note de Shepard", command = create_note_shepard)
filemenu.add_cascade(label="Nouveau", menu= newmenu)

filemenu.add_command(label="Ouvrir", command=open_son)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Fichier", menu=filemenu)

root.config(menu=menubar)
mainloop()
