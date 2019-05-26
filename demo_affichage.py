import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
import os
import son
import shepard
import matplotlib.pyplot as plt
from tkinter import filedialog

def grapheFFT(don):
   don.graphFFT()

def decalFFT(don, entr1, entr2, entr3):
   don.decalFFT(int(entr1), [int(entr2) , int(entr3)])
   don.graphFFT()

def ecrire_wav(don, e2):
   don.ecrire(e2)
   
def add_some_action(don):
   addaction = Toplevel(root)
   TEXTE = "Vous venez de créer un fichier son. Si vous souhaitez visualiser le module de la transformée de fourier, cliquez sur le boutton ci-dessous:"
   Label(addaction, text = TEXTE).grid(row=0)
   Button(addaction, text='Afficher le graphe FFT', command= lambda : don.graphFFT()).grid(row=1, column=1, sticky=W, pady=4)
   TEXTE2 = "Si vous souhaitez décaler la plage de fréquence, veuillez remplir les champs ci-dessous."
   Label(addaction, text = TEXTE2).grid(row=2)
   entry1 = Entry(addaction)
   entry1.grid(row=3, column=1)
   Label(addaction,text= "Fréquence : ").grid(row=2, column=1)
   
   entry2 = Entry(addaction)
   entry2.grid(row=3, column=2)
   Label(addaction,text= "Plage de fréquence, à gauche fmin, à droite fmax : ").grid(row=2, column=2)
   
   entry3= Entry(addaction)
   entry3.grid(row=3, column=3)
   
   Button(addaction, text='Inverser le graphe FFT', command= lambda : decalFFT(don, entry1.get(), entry2.get(), entry3.get())).grid(row=4, column=1, sticky=W, pady=4)
   TEXTE3 = "Si vous souhaitez créer un fichier au format .wav correspondant à l'objet crée veuillez remplir le champ ci dessous afin de lui donner un nom."
   Label(addaction, text = TEXTE2).grid(row=5)
   Label(addaction, text="Nom du fichier .wav : ").grid(row=6)
   e2 = Entry(addaction)
   e2.grid(row=6, column=1)
   try:
      Button(addaction, text='Créer le fichier .wav', command= lambda : ecrire_wav(don, e2.get() )).grid(row=7, column=1, sticky=W, pady=4)
   except AttributeError:
      pass
   Label(addaction, text="Pour visualiser le spectrogramme de l'objet, veuillez cliquer ici :").grid(row=8)
   Button(addaction, text="Afficher le spectrogramme", command = lambda : don.spectro()).grid(row=8, column = 1, sticky=W, pady=4) 
   Button(addaction, text='Quit', command=addaction.quit).grid(row=9, column=0, sticky=W, pady=4)  

def create_son(e1):
   donnee2 = shepard.note(int(e1))   
   print("Création de la note de fréquence fondamentale", int(e1))
   add_some_action(donnee2)

def create_son_shepard(e1):
   donnee = shepard.noteShepard(int(e1))
   print("Creation de la note de Shepard de fréquence fondamentale", int(e1))
   add_some_action(donnee)

def create_note_shepard():
   createshepard = Toplevel(root)
   TEXTE = "Le nombre d'octet est fixé à 2. La durée est fixée à 3 secondes et le volume est à 0.5."
   Label(createshepard, text = TEXTE).grid(row=0)
   Label(createsheapard, text="Fréquence fondamentale de la note (Hz) : ").grid(row=1)
   e1 = Entry(createshepard)
   e1.grid(row=1, column=1)  
   Button(createshepard, text='Créer la note de Shepard', command= lambda : create_son_shepard(e1.get())).grid(row=3, column=1, sticky=W, pady=4)
   Button(createshepard, text='Quit', command=createshepard.quit).grid(row=3, column=0, sticky=W, pady=4)   
   
def create_note():
   createnote = Toplevel(root)
   TEXTE = "Le nombre d'octet est fixé à 2 et la fréquence d'échantillonnage est déjà fixée à 44 100 Hz. La durée est fixée à 3 secondes et le volume est à 0.5."
   Label(createnote, text = TEXTE).grid(row=0)
   Label(createnote, text="Fréquence fondamentale de la note (Hz) : ").grid(row=1)
   e1 = Entry(createnote)
   e1.grid(row=1, column=1)  
   Button(createnote, text='Créer le son', command= lambda : create_son(e1.get())).grid(row=3, column=1, sticky=W, pady=4)
   Button(createnote, text='Quit', command=createnote.quit).grid(row=3, column=0, sticky=W, pady=4)
   
def open_data(e1):
   var = son.ouvrir(e1)
   print(var.fech)
   add_some_action(var)

def open_son():
   open = Toplevel(root)
   open.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("wav files","*.wav"),("all files","*.*")))
   print (open.filename)
   open_data(open.filename)
   
   #Button(openson, text='Quitter', command=openson.quit).grid(row=3, column=0, sticky=W, pady=4)
   #Button(openson, text='Ouvrir le fichier', command= open_data(e1.get()) ).grid(row=3, column=1, sticky=W, pady=4)
   
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
