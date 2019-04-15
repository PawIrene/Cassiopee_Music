# -*- coding: utf-8 -*-
"""
Ce module permet de générer des objets donnees_son representant des sons de Shepard.
"""

import son
import numpy as np

def note(fNote,nbOctet=2,fech=44100,duree=3,volume=0.5):
    """
    Renvoie l’objet donnees_son correspondant a une sinusoide pure de frequence
    fNote avec les parametres de pas de quantification, de frequence 
    d’echantillonnage, de duree et de volume entre.
    
    - fNote float positif en Hz
    - nbOctet un entier entre 1 et 2
    - fech entiers positifs en Hz
    - duree en s positive
    - volume float entre 0 et 1
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
            data[i] = (int(128 + 127*volume*np.sin(2*np.pi*fNote*i/fech)))
    else: #nbOctet == 2
        for i in range(len(data)):
            data[i] = (int(32767*volume*np.sin(2*np.pi*fNote*i/fech)))
    return son.DonneeSon(data,nbOctet,fech)
    
    
    
def noteShepard(fFond, nbOctet = 2, duree = 3, volume = 0.5):
    """
    Renvoie l’objet donnees_son correspondant a une note de Shepard de 
    fondamentale fFond en Hertz.
    
    - fFond en Hz des entiers positifs
    - duree en s positive
    - volume float entre 0 et 1
    - nbOctet un entier entre 1 et 2
    """
    while(fFond>31):
        fFond = fFond//2 #on s'assure que la note fait partie de la game -1
    fech = 44100
    listeHarmo = [[]]*10 #la liste des differentes harmoniques audibles
    for i in range(len(listeHarmo)):
        listeHarmo[i] = note(fFond*(2**i),nbOctet,fech,duree,volume).data
    data = [0]*(int(duree*fech))
    for i in range(len(data)):
        somme = 0
        for j in range(len(listeHarmo)):
            somme += listeHarmo[j][i]
        data[i] = somme//10
    return son.DonneeSon(data,nbOctet,fech)


   

def gammeShepard(listFond=[16.35*2**(float(i)/12) for i in range(12)],\
nbOctet=2,fech=44100,dureeNote=0.35,dureeSilence=0.15,volume=0.5):
    
    """
    Renvoie l’objet donnees_son correspondant a un enchainement de notes de 
    Shepard. Permet de tester l’illusion auditive.
    
    - duree en s positive
    - dureeSilence en s positive
    - volume float entre 0 et 1
    - nbOctet un entier entre 1 et 2
    - fech en Hz entier positif
    - listFond un tableau contenant dans l'ordre chronologique la liste
    des valeurs en Herz des fondamentales des notes de chepard desirees
    """
    
    data = []
    silence = [0]*int(fech*dureeSilence)
    for j in range(len(listFond)):
        data += noteShepard(listFond[j],nbOctet,dureeNote,volume).data + silence
    return son.DonneeSon(data,nbOctet,fech)
