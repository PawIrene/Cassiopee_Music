# -*- coding: utf-8 -*-
"""
Ce module permet de definir les objets donnees_son.
"""

import wave
import os.path
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import sys


def ouvrir(nom):
    """
    Si nom est une chaine de caractere correspondant a un ficher wave 
    (avec ou sans l'extension), renvoie l’objet donnees_son correspondant a ce 
    fichier sonore.
    Gere la conversion stereo vers mono
    """
    assert(type(nom)==str),"chaine de charactere attendue pour nom"
    
    if(nom[-4:]!=".wav"):
        nom+=".wav"
    
    with wave.open(nom,'r') as fichier: #creation de l'objet type Wave_read
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
                valeur_ech = int.from_bytes(data_byte[i:i+2], \
                                            byteorder='little', signed=True)
                data.append(valeur_ech)
                i=i+2
        #conversion stereo vers mono si besoin
        if(fichier.getnchannels()==2):
            dataMono = [(data[n]+data[n+1])//2 for n in range(0,len(data)-2,2)]
            data = dataMono
            print("Conversion de stereo vers mono effectuee")
        fech = fichier.getframerate()
        objet = DonneeSon(data,nbOctet,fech)
    print("Donnees de {} recuperes.\nCaracteristiques : duree = {}s, \
fech = {}, nbOctet = {} ".format(nom,round(len(data)/fech,2),\
          fech,nbOctet))
    return objet
    

class DonneeSon:
    """
    objet DonneeSon
        -data le tableau des valeurs des echantillons
        -nbOctet = 1 ou 2 le nombre d'octets utilise par echantillon
        -fech la frequence d'echantillonnage
    """
    def __init__(self,data,nbOctet,fech):
        self.data=data
        self.nbOctet=nbOctet
        self.fech=fech
    
    def ecrire(self,nom):
        """
        Cree, sous le nom nom, le fichier au format wave 
        correspondant a l’objet.
        """
        assert (type(nom) == str),"nom doit etre une chaine de charactere"
        if(nom[-4:]!=".wav"):
            nom+=".wav"
        assert (not(os.path.exists(nom))), \
        "le fichier " +nom +" existe déjà"
        
        fichier = wave.open(nom,'w') #creation de l'objet type Wave_write
        nbEch = len(self.data)
        fichier.setparams((1, self.nbOctet, self.fech, nbEch, "NONE", \
                           "not compressed" ))
        print("creation du fichier en cours...")
        if(self.nbOctet == 1):
            encodage='B'
        else:
            encodage='h'
        for i in range(nbEch):
            fichier.writeframes(wave.struct.pack(encodage,self.data[i]))
            
            if((i%500)==0): #pour afficher la progression
                raffraichirProgres(i/nbEch)
                
        raffraichirProgres(1)
        fichier.close()
                
        #la duree est egale au nombre d'échantillon divise par fech.
        duree = nbEch/(self.fech)
        print("le fichier {} de duree {}s a ete cree".format\
              (nom,round(duree,2)))
        
    def copie(self):
        """
        Retourne une copie de l'objet DonneeSon.
        Utile pour conserver des versions de l'objet avant les traitements.
        """
        dataCp = [elt for elt in self.data]
        return(DonneeSon(dataCp,self.nbOctet,self.fech))
        
    
    def ssEch(self,info=1,N=2):
        """
        Si la fech est bien multiple de N, modifie l’objet de maniere a 
        obtenir sa version sous-echantillonnee a fech/N.
        
        Si info==1, informe via la console les possibilites pour N et attend un
        choix. Sinon, prend en compte le paramètre N entre lors de l'appel.
        """
        if(info==1):
            print("La frequence d'echantillonage actuelle est de {} Hz."\
                  .format(self.fech))
            print("\nLe facteur de reduction N peut prendre une valeur \
dans la liste suivante:")
            liste = diviseurs(self.fech)
            print("{}".format(liste))
            N=int(input("Votre choix pour N (1 pour annuler):"))
        assert (type(N)==int and N>0),"N doit etre un entier strictement positif"
        assert (self.fech%N==0),\
        "la frequence d'echantillonage n'est pas divisible par N"
        if(N>1):#on annule si N vaut 1
            self.fech=(self.fech//N)
            newdata = []
            for i in range(len(self.data)):
                if(i%N==0):
                    newdata.append(self.data[i])
            self.data = newdata
            print("Nouvelle fech = {}".format(self.fech))
        
    def ssOct(self):
        """
        Si self représente des valeures codées sur 2 octets, réduit le pas
        de quantification pour obtenir un codage sur 1 octet.
        """
        
        assert (self.nbOctet==2),"Déjà quantifié sur un octet"
        
        for i in range(len(self.data)):
            self.data[i] = int((self.data[i]+32768)*(255/65535))
        self.nbOctet = 1
    
    def ssPas(self,N=2):
        """
        Permet d'observer les effets d'une quantification plus grossière.
        Fixe le nombre d'octet par échantillon à 1 pour avoir 256 niveaux
        puis arrondi les valeurs de manière à ne garder que 256//N niveaux.
        
        ATTENTION : perte de qualité sans gain en espace de stockage ou vitesse
                    de traitement !
        
        - N entier entre 2 et 50, qui permet un nombre de niveau de quantification
          entre 128 et 5.
        """
        assert ((type(N)==int)and(N>1)and(N<=50)),\
        "N doit etre entier entre 2 et 50"
        if(self.nbOctet==2):
            self.ssOct()        
        for i in range(len(self.data)):
            val = self.data[i]
#On réduit la valeur jusqu'à en obtenir une dans la liste des valeurs quantifiés
            while(((val>0)and(val%N!=0))or(val>(255-N))):
                val-=1
            self.data[i]=val
        print("Nombre de niveau de quantification reduit a {}".format(256//N))
    
    def dB(self,valeurdB):
        """
        Augmente ou diminue le volume sonore de l'objet de valeurdB,
        si ce flottant est respectivement positif ou negatif.
        Alarme l'utilisateur en cas de risque de saturation lors de l'etape
        d'ecriture.
        """
        assert(type(valeurdB)==float or type(valeurdB)==int),"Flottant attendu"
        
#valeur trouvee experimentalement pour rapport de puissance en dB du format wave :
        const_dB = 0.113129
        if(self.nbOctet==1): #on passe en mode valeurs positives et negatives
            Ndata = [self.data[i]-128 for i in range(len(self.data))]
        else:
            Ndata = [self.data[i] for i in range(len(self.data))]
            
        if(valeurdB<0): #on diminue la puissance de valeurdB
            valeurdB*=-1
            for j in range(len(self.data)):
                self.data[j] = int(Ndata[j]/np.exp(const_dB*valeurdB))
        else:           #on augmente la puissance de valeurdB
            for j in range(len(self.data)):
                self.data[j] = int(Ndata[j]*np.exp(const_dB*valeurdB))
                
        if(self.nbOctet==1): #on revient au format de donnees wave pour 1 octet
            self.data = [self.data[i]+128 for i in range(len(self.data))]
            if(max(self.data)>255 or min(self.data)<0):
                print("ATTENTION : saturation prevue au moment de l'ecriture")
        else:
            if(max(self.data)>32767 or min(self.data)<-32676):
                print("ATTENTION : saturation prevue au moment de l'ecriture")
        print("Nouvelle valeur max = {}, nouvelle valeur min = {}"\
              .format(max(self.data),min(self.data)))    

                
    
    def formeGraphTemps(self):
        """
        Renvoie un tableau de 2 tableaux [t,y]. 
        - Le premier element du tableau est le tableau x representant la valeur
        du temps en s. 
        - Le second element est le tableau y representant les valeurs des 
        echantillons correspondantes.
        """
        
        Te = 1/self.fech
        t = [i*Te for i in range(len(self.data))]
        return [t,self.data]
        
    
#__________________________Partie_Fourrier_____________________________________

    
    def formGraphFFT(self,fmin=0,fmax=22100):
        """
        Renvoie un tableau de 2 tableaux [f,Y]. 
        - Le premier element du tableau est le tableau f representant la valeur
        des frequences en Hz.
        Le second element est le tableau Y representant le module des valeurs des 
        echantillons correspondantes dans le domaine de Fourier une fois normalise.
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
    
    def graphFFT(self,nom="courbeFFT",tmin=0,tmax=0.02,fmin=0,fmax="fech//2"):
        """
        Permet de visualiser le module de la transformee de fourier normalise
        en regard de la forme d'onde.
        La plage des ordonnees affichees s'adapte aux valeurs max de la courbe.
        - nom une string qui sera le nom de la courbe ajoutee
                (utile si visualisation parallèle de plusieurs courbes)
        - tmin et tmax en s
        - fmin et fmax en Hz
        """
        if(fmax=="fech//2"):
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
        plt.plot(f,Y,label=nom)
        plt.axis([fmin,fmax,-0.2,1.2])
        plt.ylabel("module de la fft")
        plt.legend()
        plt.show()


        
    def inverseFFT(self):
        """
        Modifie l’objet de maniere a realiser l’operation d’inversion du spectre 
        (on inverse le signe des echantillons une fois sur deux)
        """
        if(self.nbOctet==2): #code sur 2 octet, donc signed
            inverse = \
            [(-1)**((n-1)%2)*(self.data[n]) for n in range(0,len(self.data))]
        else: #code entre 0 et 255
            inverse = []
            for n in range(0,len(self.data)):
                if(n%2):
                    inverse.append(self.data[n])
                else:
                    inverse.append(256-self.data[n]) #equivalent du negatif           
        self.data = inverse
        
    def decalFFT(self,f,plage=[70,350]):
        """
        Modifie l’objet de maniere a obtenir les echantillons correspondant à 
        un decalage de la plage de frequence plage de f herz. f peut etre negatif.
        """
        assert((f+plage[0])>0),"la borne inferieur de la plage est trop basse"
        assert((f+plage[1])<(len(self.data)//2)),\
        "la borne superieure de la plage est trop haute"
        assert(f!=0),"entrer une frequence non nulle"
        
        duree = len(self.data)/(self.fech)
        idecal = int(f*duree) #correspond au nombre d'indice du decallage
        iplage=[int(plage[0]*duree),int(plage[1]*duree)]
        # definition de a, les donnees au format array
        a = np.asarray(self.data)
        
        A = np.fft.rfft(a)
        #on decalle les indices des valeurs du spectre de fourier des frequences positive
        if(idecal>=0):
            for i in range(iplage[1],iplage[0],-1):
                A[i+idecal]=A[i]
                A[i]=0j
                A[len(A)-i-idecal]=A[len(A)-i]
                A[len(A)-i]=0j
        else:
        #on décalle les indices des valeurs du spectre de fourier des frequences negatives
            for i in range(iplage[0],iplage[1]):
                A[i+idecal]=A[i]
                A[i]=0j
                A[len(A)-i-idecal]=A[len(A)-i]
                A[len(A)-i]=0j
        a=np.fft.irfft(A)
        self.data = [int(a[i]) for i in range(len(a))]
    
    def filtreBas(self,coupure, ordre = 200):
        """
        Réalise un filtrage numérique passe bas RIF à l'aide d'une
        fenêtre de Hamming.
        
        coupure : la frequence de coupure en Hz
        ordre : l'ordre du filtre
        """
        assert(type(coupure)==float or type(coupure)==int),\
        "Flottant en HZ attendu pour l'argument coupure"
        assert(type(ordre)==int),\
        "ordre doit etre un entier representant l'ordre desire du filtre"
        
        coupure = 2*coupure/self.fech #par convention frequence de nyquyst = 1
        filtre = sig.firwin(ordre,coupure)
        res = sig.convolve(self.data,filtre,mode="same")
        self.data = [int(res[i]) for i in range(len(res))]
    
    def visufiltreBas(self, coupure, ordre=200):
        """
        Pour observer la reponse frequentielle du filtreBas applique
        avec les memes parametres
        """
        coupure = 2*coupure/self.fech #par convention frequence de nyquyst = 1
        filtre = sig.firwin(ordre,coupure)
        visuFiltre(filtre,self.fech)
        
        
    def filtreHaut(self, coupure, ordre = 200):
        """
        Réalise un filtrage numérique passe haut RIF à l'aide d'une
        fenêtre de Hamming.
        
        coupure : la frequence de coupure en Hz
        ordre : l'ordre du filtre
        """
        assert(type(coupure)==float or type(coupure)==int),\
        "Flottant en HZ attendu pour l'argument coupure"
        assert(type(ordre)==int),\
        "ordre doit etre un entier representant l'ordre desire du filtre"
        if(ordre%2==0):
            ordre += 1 #on évite une contrainte dans lec as de l'odre pair
        coupure = 2*coupure/self.fech #par convention frequence de nyquyst = 1
        filtre = sig.firwin(ordre,coupure,pass_zero=False)
        res = sig.convolve(self.data,filtre,mode="same")
        self.data = [int(res[i]) for i in range(len(res))]
        
    def visufiltreHaut(self, coupure, ordre=200):
        """
        Pour observer la reponse frequentielle du filtreHaut applique
        avec les memes parametres
        """
        if(ordre%2==0):
            ordre += 1 #on évite une contrainte dans le cas de l'odre pair
        coupure = 2*coupure/self.fech #par convention frequence de nyquyst = 1
        filtre = sig.firwin(ordre,coupure,pass_zero=False)
        visuFiltre(filtre,self.fech)
        
    def filtreBande(self, coupure, passe_bande=True, ordre = 200):
        """
        Réalise un filtrage numérique RIF à l'aide d'une
        fenêtre de Hamming. Si passe_bande == True on effectue un filtrage
        passe_bande, s'il vaut False on effectue un filtrage coupe bande.
        
        
        coupure : tableau des deux frequence de coupure en Hz
        passe_bande : Booleen pour choisir passe ou coupe bande
        ordre : l'ordre du filtre
        """
        assert(len(coupure)==2),\
        "Tableau de 2 frequence en herz [f0, f1] attendu pour l'argument coupure"
        assert(type(passe_bande)==bool), \
        "Booleen attendu pour l'argument passe_bande"
        assert(type(ordre)==int),\
        "ordre doit etre un entier representant l'ordre desire du filtre"
        
        if(ordre%2==0 and not(passe_bande)):
            ordre += 1 #on évite une contrainte dans le cas de l'odre pair
        coupure[0] = 2*coupure[0]/self.fech #par convention frequence de nyquyst = 1
        coupure[1] = 2*coupure[1]/self.fech
        filtre = sig.firwin(ordre,coupure,pass_zero=not(passe_bande))
        res = sig.convolve(self.data,filtre,mode="same")
        self.data = [int(res[i]) for i in range(len(res))]

    def visufiltreBande(self, coupure, passe_bande = True, ordre=200):
        """
        Pour observer la reponse frequentielle du filtreHaut applique
        avec les memes parametres
        """
        if(ordre%2==0):
            ordre += 1 #on évite une contrainte dans le cas de l'odre pair
        coupure[0] = 2*coupure[0]/self.fech #par convention frequence de nyquyst = 1
        coupure[1] = 2*coupure[1]/self.fech
        filtre = sig.firwin(ordre,coupure,pass_zero=not(passe_bande))
        visuFiltre(filtre,self.fech)

#__________________________Partie_Spectrogramme________________________________

    def spectro(self,nom="spectrogramme"):
        
        plt.figure()
        plt.title(nom)
        if(self.nbOctet!=2):  #Pour eviter la composante continue parasite
            donnee = [(elt-128) for elt in self.data]
        else:
            donnee = self.data
        plt.specgram(donnee,Fs=self.fech)
        plt.xlabel("temps(s)")
        plt.ylabel("frequence(Hz)")
        plt.grid()
        plt.show()

#__________________________Partie_Effets_Sonor_________________________________

    def compression(self,seuil=2,taux=3):
        """
        Applique un algorithme simple de compression audio.
        La dynamique du signal est reduite a partir du moment ou
        seuil est dépassé. 
        Un depassement relatif de taux dB a partir du seuil sera reduite a 1db, 
        une augmentation de 2*taux sera reduite a 2dB etc...
            
        Sortie = seuil + [Entree-seuil]/taux
        
            -seuil : flottant positif en dB. On place le seuil de maniere
                    a ce qu'il corresponde a un son d'une puissance egale a
                    la valeur de puissance maximale prise par le fichier audio
                    attenue de cette valeure entree.
                    
            -taux : flottant positif representant l'attenuation a appliquer en dB
        """
        
#valeur trouvee experimentalement pour rapport de puissance en dB du format wave :
        const_dB = 0.113129 
        if(self.nbOctet==1):
            #on place les seuils à valeur maximum diminué de seuil dB
            valMaxi=max([abs(self.data[i]-127) for i in range(len(self.data))])
            valSeuilmax = int(127 + valMaxi/np.exp(const_dB*seuil))
            valSeuilmin = int(127 - valMaxi/np.exp(const_dB*seuil))
        else:
            valMaxi = max([abs(self.data[i]) for i in range(len(self.data))])
            valSeuilmax = int(valMaxi/np.exp(const_dB*seuil))
            valSeuilmin = int(-valMaxi/np.exp(const_dB*seuil)) 
        for n in range(0,len(self.data)):
#on réduit la différence de puissance avec le seuil de taux dB.
            if(self.data[n]>valSeuilmax):
                self.data[n]=valSeuilmax\
                +int((self.data[n]-valSeuilmax)/np.exp(const_dB*seuil))
                
            elif(self.data[n]<valSeuilmin):
                self.data[n]=valSeuilmin\
                +int((self.data[n]-valSeuilmin)/np.exp(const_dB*seuil))
#on informe l'utilisateur des caracteristiques du resultat
        if(self.nbOctet==1):
            NvalMaxi=max([abs(self.data[i]-127) for i in range(len(self.data))])
        else:
            NvalMaxi = max([abs(self.data[i]) for i in range(len(self.data))])
        print("AncienMax = {}, valSeuil = {}, NouveauMax = {}".format(\
              valMaxi,valSeuilmax,NvalMaxi))
        

#__________________________Utilitaire__________________________________________
                
                
def raffraichirProgres(progres):
    """
    Affiche ou met a jour une barre de progression.
    Accepte un flottant entre 0 et 1. Les entiers sont convertis en flottant.
    Une valeur negative affiche "arret".
    Une valeur a 1 ou plus represente 100%
    Principe de la fonction trouve sur Stack Overflow.
    """
    barreLong = 10 # Modifier pour changer la taille de la barre de progres
    status = ""
    if isinstance(progres, int):
        progres = float(progres)
    if not isinstance(progres, float):
        progres = 0
        status = "erreur: variable progres doit etre flottant\r\n"
    if progres < 0:
        progres = 0
        status = "Arret\r\n"
    if progres >= 1:
        progres = 1
        status = "Fait!\r\n"
    block = int(round(barreLong*progres))
    text = "\rProgres: [{0}] {1}% {2}"\
    .format("#"*block + "-"*(barreLong-block), int(progres*100), status)
    sys.stdout.write(text)
    sys.stdout.flush()
    
    
    
def diviseurs(n):
    """
    Renvoie la liste des 10 premiers diviseurs de l'argument n, entier positif
    (1 et n exclus)
    """
    assert(type(n)==int and n>=0),"un entier positif est attendu pour n"
    
    div=[];
    i=1
    while(i<(n-1) and len(div)<10):
        i+=1
        if n % i == 0:
            div.append(i)

    return div

def visuFiltre(filtre, fech):
    """
    Utilise pour les fonctions de visualisation de visufiltreHaut, visufiltreBas 
    et visufiltreBande
    """
    
    w,h=sig.freqz(filtre)
    plt.figure()
    plt.subplot(211)
    plt.plot(fech*w/(np.pi*2),20*np.log10(np.absolute(h)))
    plt.xlabel("f(Hz)")
    plt.ylabel("Gain(dB)")
    plt.grid()
    plt.subplot(212)
    plt.plot(fech*w/(2*np.pi),np.unwrap(np.angle(h)))
    plt.xlabel("f(Hz)")
    plt.ylabel("phase(rad)")
    plt.grid()
    plt.show()
