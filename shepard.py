# -*- coding: utf-8 -*-
"""
Ce module permet de realiser des tableaux d'entier directement exploitable par le module wav.py pour manipuler les sons de Shepard.
"""
import wav as w
import math as m

def note(fNote, fech=44100, duree=3, volume=0.5, nbOctet=2):
    """
    retourne le tableau d entier correspondant a une sinusoide pure
    de frequence fNote echantillonee a fech en Hz quantifie sur nbOctet sur une
    duree de duree s.
    
    fNote float positif en Hz
    fech entiers positifs en Hz
    duree en s positive
    volume float entre 0 et 1
    nbOctet un entier entre 1 et 2
    """
    
    assert (type(fech) == int and fech > 0),"la frequence d echantillonage\
    doit etre un entier positif"
    assert (fNote >= 0),"la frequence de la note doit etre un float positif"
    assert (duree >= 0),"la duree de la note\
    doit etre un nombre flotant positif de secondes"
    assert (type(nbOctet)==int and (nbOctet==1 or nbOctet==2)),\
"le nombre d'octet par echantillon doit valoir 1 ou 2"
    assert (0<=volume<=1),"volume doit etre compris entre 0 et 1"
    
    
    
    data = [0]*(int(duree*fech))
    if(nbOctet == 1):
        for i in range(len(data)):
            data[i] = (int(128 + 127*volume*m.sin(2*m.pi*fNote*i/fech)))
    else: #nbOctet == 2
        for i in range(len(data)):
            data[i] = (int(32767*volume*m.sin(2*m.pi*fNote*i/fech)))
    return data
    
    
    
def noteShepard(fFond, duree=1, volume=0.5, nbOctet=2):
    """
    retourne le tableau d entier correspondant a la note de Shepard
    de frequence fondamentale fNote en HZ echantillonee a 44100Hz quantifie sur 
    nbOctet sur une duree de duree s.
    
    fNote et fech en Hz des entiers positifs
    duree en s positive
    volume float entre 0 et 1
    nbOctet un entier entre 1 et 2
    """
    
    fech = 44100
    listeHarmo = [[]]*10 #la liste des différetes harmoniques audibles
    for i in range(len(listeHarmo)):
        listeHarmo[i] = note(fFond*(2**i),fech,duree,volume,nbOctet)
    data = [0]*(int(duree*fech))
    for i in range(len(data)):
        somme = 0
        for j in range(len(listeHarmo)):
            somme += listeHarmo[j][i]
        data[i] = somme//10
    return data


   

def gammeShepard(nbRepet=1,dureeNote=1,dureeSilence=1,volume=0.5,nbOctet=2\
,listFond=[16.35*2**(i/12) for i in range(12)]):
    """
    retourne le tableau d entier correspondant a la gamme de Shepard
    echantillonee a 44100Hz quantifie sur nbOctet repetee nbRepet fois
    avec des duree de note de dureeNote secondes et des silences de
    dureeSilence secondes.
    
    nbRepet entier positif
    duree en s positive
    dureeSilence en s positive
    volume float entre 0 et 1
    nbOctet un entier entre 1 et 2
    """
    
    data = []
    silence = note(0, 44100, dureeSilence, 0, nbOctet)
    for i in range(nbRepet):
        for j in range(len(listFond)):
            data += noteShepard(listFond[j],dureeNote,volume,nbOctet) + silence

    return data 
