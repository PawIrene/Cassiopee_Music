# -*- coding: utf-8 -*-
"""
Ce module permet de définir les objets donnees_son.
"""

import wave
import os.path
import numpy as np
import matplotlib.pyplot as plt

def ouvrir(nom):
    """
    Si nom est une chaîne de caractère correspondant à un ficher wave 
    (sans l'extension), renvoie l’objet donnees_son correspondant à ce fichier sonore.
    """
    with wave.open(nom + ".wav",'r') as fichier: #creation de l'objet type Wave_read
     #on recupere les donnees brut au format byte_elt (pas l'en-tete) :
        data_byte=fichier.readframes(fichier.getnframes())
        data_length = len(data_byte) #nb d'octets de donnees
        nbOctet = fichier.getsampwidth() #echantillon code sur 1 ou 2 octets
        if(nbOctet == 1): #la conversion pour 1 octet est directe
            data = [data_byte[i] for i in range(data_length)]
        else: #on regle la conversion dans le cas de deux octet + signe :
            i=0
            data = []
            while i < data_length:
                valeur_ech = int.from_bytes(data_byte[i:i+2], byteorder='little', signed=True)
                data.append(valeur_ech)
                i=i+2
                
        fech = fichier.getframerate()
        objet = DonneeSon(data,nbOctet,fech)
    return objet
    


class DonneeSon:
    """
    objet DonneeSon
        -data le tableau des valeurs des echantillons
        -nbOctet = 1 ou 2 le nombre d'octets utilisé par échantillon
        -fech la frequence d'echantillonnage
    """
    def __init__(self,data,nbOctet,fech):
        self.data=data
        self.nbOctet=nbOctet
        self.fech=fech
    
    def ecrire(self,nom):
        """
        Créé, sous le nom nom, le fichier au format wave 
        correspondant à l’objet.
        """
        assert (type(nom) == str),"nom doit etre une chaine de charactere"
        assert (not(os.path.exists(nom+".wav"))), "le fichier " +nom +".wav existe déjà"
        
        fichier = wave.open(nom + ".wav",'w') #creation de l'objet type Wave_write
        nbEch = len(self.data)
        fichier.setparams((1, self.nbOctet, self.fech, nbEch, "NONE", "not compressed" ))
        print("creation du fichier en cours...")
        if(self.nbOctet == 1):
            encodage='B'
        else:
            encodage='h'
        for i in range(1,nbEch):
            fichier.writeframes(wave.struct.pack(encodage,self.data[i]))
        fichier.close()
                
        #la duree est egale au nombre d'échantillon divise par fech.
        duree = nbEch/(self.fech)
        print("le fichier {0}.wav de duree {1}s a ete cree".format(nom,round(duree,2)))
    
    def ssEch(self,N=2):
        """
        Si le nombre d’échantillons de l’objet est bien multiple de N, modifie 
        l’objet de manière à obtenir sa version sous-échantillonnée à fech/N.
        """
        assert (type(N)==int),"N doit être un entier"
        assert (self.fech%N==0),"la frequence d'echantillonage n'est pas divisible par N"
        self.fech=(self.fech//N)
        newdata = []
        for i in range(len(self.data)):
            if(i%N==0):
                newdata.append(self.data[i])
        self.data = newdata
                
    
    def formeGraphTemps(self):
        """
        Renvoie un tableau de 2 tableaux [t,y]. 
        - Le premier élément du tableau est le tableau x représentant la valeur
        du temps en s. 
        - Le second élément est le tableau y représentant les valeurs des 
        échantillons correspondantes.
        """
        
        Te = 1/self.fech
        t = [i*Te for i in range(len(self.data))]
        return [t,self.data]
        
    
#__________________________Partie_Fourrier_____________________________________

    
    def formGraphFFT(self,fmin=0,fmax=22100):
        """
        Renvoie un tableau de 2 tableaux [f,Y]. 
        - Le premier élément du tableau est le tableau f représentant la valeur
        des fréquences en Hz.
        Le second élément est le tableau Y représentant le module des valeurs des 
        échantillons correspondantes dans le domaine de Fourier une fois normalisé.
        """
        # definition de y, les donnees au format array
        y = np.asarray(self.data)
        # calcul de Y
        Y = np.fft.fft(y)
        #pour normaliser l'amplitude dans le domaine frequenciel sans tenir compte
        #de la composante continue
        norm = max(np.abs(Y[1:]))
        # mise a la bonne echelle des frequences a partir de la duree
        duree = len(self.data)/(self.fech)
        f = np.linspace(0,len(Y)/duree,len(Y))
        return [f,np.abs(Y)/norm]
    
    def graphFFT(self,tmin=0,tmax=0.02,fmin=0,fmax=0):
        """
        Permet de visualiser le module de la transformee de fourier en regard de
        la forme d'onde.
        
        - tmin et tmax en s
        - fmin et fmax en Hz
        """
        if(fmax==0):
            fmax = (self.fech//2)
        
        formeTemps = self.formeGraphTemps()
        formeFFT = self.formGraphFFT()
        t = formeTemps[0]
        y = formeTemps[1]
        
        f = formeFFT[0]
        Y = formeFFT[1]
        
        # visualisation de y
        plt.subplot(211)
        plt.plot(t,y)
        plt.axis([tmin,tmax,min(y),max(y)])
        plt.ylabel("forme d'onde")
        
        
        # visualisation de A
        plt.subplot(212)
        plt.plot(f,Y)
        plt.axis([fmin,fmax,-0.2,1.2])
        plt.ylabel("module de la fft")
        
    def inverseFFT(self):
        """
        Modifie l’objet de manière à réaliser l’opération d’inversion du spectre 
        (on inverse le signe des échantillons une fois sur deux)
        """
        if(self.nbOctet==2): #code sur 2 octet, donc signed
            inverse = [(-1)**((n-1)%2)*(self.data[n]) for n in range(1,len(self.data))]
        else: #code entre 0 et 255
            inverse = []
            for n in range(1,len(self.data)):
                if(n%2):
                    inverse.append(self.data[n])
                else:
                    inverse.append(256-self.data[n]) #equivalent du negatif           
        self.data = inverse
        
    def decalFFT(self,f,plage=[70,350]):
        """
        Modifie l’objet de manière à obtenir les échantillons correspondant à 
        un décalage de la plage de fréquence plage de f herz (f peut être négatif).
        """
        assert((f+plage[0])>0),"la borne inférieur de la plage est trop basse"
        assert((f+plage[1])<(len(self.data)//2)),"la borne supérieure de la plage est trop haute"
        assert(f!=0),"entrer une fréquence non nulle"
        
        duree = len(self.data)/(self.fech)
        idecal = int(f*duree) #correspond au nombre d'indice du decallage
        iplage=[int(plage[0]*duree),int(plage[1]*duree)]
        # definition de a, les donnees au format array
        a = np.asarray(self.data)
        
        A = np.fft.fft(a)
        #on decalle les indices des valeurs du spectre de fourier des frequences positive
        if(idecal>=0):
            for i in range(iplage[1],iplage[0],-1):
                A[i+idecal]=A[i]
                A[i]=0j
                A[len(A)-i-idecal]=A[len(A)-i]
                A[len(A)-i]=0j
        else:
            for i in range(iplage[0],iplage[1]):
                A[i+idecal]=A[i]
                A[i]=0j
                A[len(A)-i-idecal]=A[len(A)-i]
                A[len(A)-i]=0j
#les approximations du calcul font apparaitre des parties imaginaires très faibles
        a=np.real(np.fft.ifft(A))
        self.data = [int(a[i]) for i in range(len(a))]
            
        
        
        
        
        
        