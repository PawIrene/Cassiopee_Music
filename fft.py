# -*- coding: utf-8 -*-
"""
module permettant d'afficher la FFT d'un tableau d'echantillon et de fournir d'autres fonctions comme le retournement de spectre
et le decalage de spectre d'un tableau d'echantillon
"""

import numpy as np
import matplotlib.pyplot as plt

def graphe_fft(data,tmin=0,tmax=0.02,fmin=0,fmax=22100):
    """
    Permet de visualiser le module de la transformee de fourier en regard de
    la forme d'onde.
    
    - tmin et tmax en s
    - fmin et fmax en Hz
    - data un tableau d'entier correspondant aux valeurs des échantillons.
    Le premier element du tableau est une liste contenant tout les parametres
    du fichier sonore sous la forme :
    [nchannels, sampwidth, framerate, nframes, "NONE", "not compressed" ]
    """
    fech = data[0][2]
    Te = 1/fech
    
    # definition de a, les donnees au format array
    a = np.asarray(data[1:])
    
    # visualisation de a
    
    t = [i*Te for i in range(len(a))]
    plt.subplot(211)
    plt.plot(t,a)
    plt.axis([tmin,tmax,min(a),max(a)])
    plt.ylabel("forme d'onde")
    
    # calcul de A
    A = np.fft.fft(a)
    
    # mise a la bonne echelle des frequences
    duree = data[0][3]/data[0][2] #on se sert pour cela de la duree du fichier
    f = np.linspace(0,len(A)/duree,len(A))
    
    # visualisation de A
    plt.subplot(212)
    #pour normaliser l'amplitude dans le domaine frequenciel sans tenir compte
    #de la composante continue
    norm = max(np.abs(A[1:]))
    plt.plot(f, np.abs(A)/norm)
    plt.axis([fmin,fmax,-0.2,1.2])
    plt.ylabel("module de la fft")

def inverse_fft(data):
    """
    Renvoie le tableau d'entiers correspondant aux valeurs des echantillons du
    signal avec le spectre inverse.
    
    - data le tableau d'entiers entrant dont les frequences doivent etre
    inversees
    """
    if(data[0][1]==2): #code sur 2 octet, donc signed
        inverse = [(-1)**((n-1)%2)*(data[n]) for n in range(1,len(data))]
    else: #code entre 0 et 255
        inverse = []
        for n in range(1,len(data)):
            if(n%2):
                inverse.append(data[n])
            else:
                inverse.append(256-data[n]) #equivalent du negatif           
    return [data[0]] + inverse

def decal_fft(data,f):
    """
    Renvoie le tableau d'entiers correspondant aux valeurs des echantillons du
    signal avec le spectre decalle de f.
    
    - data le tableau d'entiers entrant dont les frequences doivent etre
    inversees
    - f en Hz positif ou négatif
    """
    
    duree = data[0][3]/data[0][2]
    idecal = int(f*duree) #correspond au nombre d'indice du decallage
    
    # definition de a, les donnees au format array
    a = np.asarray(data[1:])
    
    A = np.fft.fft(a)
    tabdecal = np.zeros(len(A)).astype(complex)
    #on decalle les indices des valeurs du spectre de fourier des frequences positive
    if(idecal>=0):
        for i in range(idecal,len(A)//2):
            tabdecal[i]=A[i-idecal]
    else:
        for i in range(0,len(A)//2-idecal):
            tabdecal[i]=A[i-idecal]
    arrayresult = np.real(np.fft.ifft(tabdecal))
    return([data[0]] + [int(arrayresult[i]) for i in range(len(arrayresult))])
