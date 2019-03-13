# -*- coding: utf-8 -*-

"""Ce module permet de manipuler des fichiers au format .wav """

import wave
import os.path

def read_wave(nom):
    """
    Lit un fichier .wav et renvoie le tableau d'entier correspondant
    aux valeurs des échantillons.
    Le premier element du tableau est un tuple contenant tout les parametres
    du fichier sonore sous la forme :
    (nchannels, sampwidth, framerate, nframes, "NONE", "not compressed" )
    
    - nom : string du nom du fichier, sans l extension .wav a la fin
    
    """
    with wave.open(nom + ".wav",'r') as fichier: #creation de l'objet type Wave_read
     #on recupere les donnees brut au format byte_elt (pas l'en-tete) :
        data_byte=fichier.readframes(fichier.getnframes())
        data_length = len(data_byte) #nb d'octets de donnees
        nbOctet = fichier.getsampwidth() #echantillon code sur 1 ou 2 octets
        if(nbOctet == 1): #la conversion pour 1 octet est directe
            resultat = [data_byte[i] for i in range(data_length)]
        else: #on regle la conversion dans le cas de deux octet + signe :
            i=0
            resultat = []
            while i < data_length:
                valeur_ech = int.from_bytes(data_byte[i:i+2], byteorder='little', signed=True)
                resultat.append(valeur_ech)
                i=i+2
                
        entete = fichier.getparams()
        params=(entete[0],entete[1],entete[2],entete[3],entete[4],entete[5])
    return [params] + resultat #on ajoute directement les info des parametre dans la liste

def new_param(nframes,nbOctet=2,fech=44100,nchannel=1):
    """
    Renvoie le tuple a mettre au debut des tableaux data permettant de
    parametrer le fichier sonor.
    
    tout les parametres attendus son des entiers :
    - nframes : le nombre total d'echantillon du fichier
    - nbOctet : 1 ou 2 octets pour quantifier un echantillon
    - fech : la frequence d echantillonnage
    - nchannel : 1 ou 2 si mono ou stereo
    """
    
    return (nchannel, nbOctet, fech, nframes,"NONE","not compressed")
    

def new_wave(nom, data=[]):
    """
    Cree le fichier wav correspondant a data.
    
    - nom : string du nom du fichier, sans l extension .wav a la fin
    
    - data : tuple d'entiers correspondant aux valeurs des échantillons.
    Le premier element du tableau est un tuple contenant tout les parametres
    du fichier sonore sous la forme :
    (nchannels, sampwidth, framerate, nframes, "NONE", "not compressed" )
    
    """
    
    assert (type(nom) == str),"nom doit etre une chaine de charactere"
    assert (type(data)==list and type(data[0])==tuple),\
    "data doit être une liste au bon format"
    assert (not(os.path.exists(nom+".wav"))), "le fichier " +nom +".wav existe déjà"
    
    
    fichier = wave.open(nom + ".wav",'w') #creation de l'objet type Wave_write
    fichier.setparams(data[0])
    print("creation du fichier en cours...")
    if(data[0][1] == 1):
        encodage='B'
    else:
        encodage='h'
    for i in range(1,len(data)):
        fichier.writeframes(wave.struct.pack(encodage,data[i]))
    fichier.close()
            
    #la duree est egale au nombre d'échantillon divise par fech.
    duree = data[0][3]/(data[0][2])
    print("le fichier {0}.wav de duree {1}s a ete cree".format(nom,round(duree,2)))
