# -*- coding: utf-8 -*-

"""Ce module permet de manipuler des fichiers au format .wav """

def read_wave(nom):
    """
    Lit un fichier .wav et affiche son contenu (format byte elements)
    
    nom : string du nom du fichier, sans l extension .wav a la fin
    
    """
    assert (type(nom)== str),"nom doit etre une chaine de charactere"
    
    with open(nom + ".wav", "rb") as fichier:
        print(fichier.read())


def new_wave(nom, data=[], fech=44100, nbOctet=2):
    """
    Cree un fichier .wav
    
    nom : string du nom du fichier, sans l extension .wav à la fin
    fech : fréquence d'échantillonage en Hz
    nbOctet : nombre d'octet pour coder la valeur d un echantillon
    data : tableau contenant la valeur des octets en decimale (de 0 à 255)
    
    """
    
    assert (type(nom) == str),"nom doit etre une chaine de charactere"
    assert (type(fech) == int and fech > 0),"la frequence d echantillonage\
    doit etre un entier positif"
    assert (type(nbOctet)==int and (nbOctet==1 or nbOctet==2)),\
"le nombre d'octet par echantillon doit valoir 1 ou 2"
    assert (type(data)==list),"data doit être une liste"
    try: #on ne créé le fichier que si il n'existe pas encore
        fichier = open(nom + ".wav", "x")
        fichier.close
    except:
        print("le fichier ",nom,".wav existe déjà")
        return 1 #on ne cree pas le fichier
    
    with open(nom + ".wav", "wb") as fichier:
        duree = len(data)/(fech)
        
        "Creation de l'en-tete :______________________________________________"
        
        fichier.write("\x52\x49\x46\x46".encode()) #Charactere 'RIFF' identifie format
        #longueur octet donnees format wave restantes sur 4 octets
        fichier.write(conv_entete(len(data)*nbOctet+48,4));
        fichier.write("\x57\x41\x56\x45\x66\x6D\x74\x20".encode()) #'WAVEfmt '
        #16 octets utilises pour defenir le format:
        fichier.write(conv_entete(16,4));
        #format de compression 1 => sans compression
        fichier.write(conv_entete(1,2));
        #nombre de canaux 1 => mono
        fichier.write(conv_entete(1,2));
        #frequence echantillonage
        fichier.write(conv_entete(fech,4));
        #debit octet/s
        fichier.write(conv_entete(fech*nbOctet,4));
        #produit nombre canaux par nombre octet par echantillon (le 1 car mono)
        fichier.write(conv_entete(1*nbOctet,2));
        #nb bit/echantillon
        fichier.write(conv_entete(8*nbOctet,2));
        fichier.write("\x66\x61\x63\x74\x04\x00\x00\x00".encode()) #'fact'puis 4
        #nombre d'echantillons
        fichier.write(conv_entete(len(data)*nbOctet,4));
        fichier.write("\x64\x61\x74\x61".encode()) #'data'
        #nombre d'echantillons
        fichier.write(conv_entete(len(data)*nbOctet,4));
        
        "on ecrit la suite de donnees au bon format :_________________________"
        isSigned = (nbOctet==2)
        for i in range(len(data)):
            octetByte =  (data[i]).to_bytes(nbOctet,'little',signed=isSigned)
            if(i==0):
                donnees = octetByte
            else :
                donnees += octetByte
        fichier.write(donnees)
    
    "on donne les infos sur le fichier :_____________________________________"
    print("creation du fichier {0}.wav de duree {1}s".format(nom,duree))

def conv_entete(valeur, nbOctet):
    """
    renvoit le byte element correspondant a la valeur pour remplir l'entete wav
    
    exemple : valeur = 65584 = 00010030h et nbOctet = 4 en entree, 
            renvoie : b'\x30\x00\x01\x00'
    
    """
    
    resHex = [0]*(nbOctet*2) #resultat intermediaire a convertir en byte elm
    resInt = [0]*nbOctet #on les replace dans l'ordre et en decimal ici
    for i in range(nbOctet*2-1,-1,-1):
        resHex[i] = valeur//(16**i)
        valeur = valeur%(16**i)
    for i in range(nbOctet):
        resInt[i] = 16*resHex[2*i+1]+resHex[2*i]
    #il ne reste plus qu'a convertir en byte element
    for i in range(nbOctet):
        ech = resInt[i].to_bytes(1,'big')
        if(i==0):
            byteElt = ech
        else :
            byteElt += ech
    return byteElt
    
