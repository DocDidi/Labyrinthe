#! /usr/bin/env python3
# coding: utf-8

import os, glob, pickle, sys, time
from var import *
if SYSTEME_D_EXPLOITATION == 'nt':
    import msvcrt
else:
    import termios, tty

def effaceEtAffiche(*valeur):
    """Efface l'écran et positionne le curseur en haut a gauche."""
    if SYSTEME_D_EXPLOITATION == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    if valeur:
        print(valeur[0])

def afficheLaby(LabyMap):
    """Affiche le labyrinthe"""
    tampon=""
    for line in LabyMap:
        for letter in line:
            if letter == LETTREMURS:
                tampon += SYMBOLEMUR
            elif letter == LETTREPORTE:
                tampon += SYMBOLEPORTE
            elif letter == LETTREFIN:
                tampon += SYMBOLEFIN
            elif letter == LETTREJOUEUR:
                tampon += SYMBOLEJOUEUR
            else:
                tampon += letter
        tampon += "\n"
    effaceEtAffiche(tampon)

def repriseSauvegarde():
    """Propose de reprendre la partie précedente"""
    if os.path.exists(FICHIERDESAUVEGARDE):
        print(MESSAGEREPRISESAUVEGARDE)
        choix = capturesaisie()
        if choix.lower() == "o":
            with open(FICHIERDESAUVEGARDE, "rb") as Sauvegarde:
                PartieEnCours = pickle.loads(Sauvegarde.read())
        else:
            os.remove(FICHIERDESAUVEGARDE)
            PartieEnCours = False
    else:
        PartieEnCours = False
    return (PartieEnCours)

def sauvegarde(LabyMap, PosJoueur, Fin, Portes):
    """Sauvegarde la partie"""
    with open(FICHIERDESAUVEGARDE, "wb") as Sauvegarde:
        Sauvegarde.write(pickle.dumps((LabyMap, PosJoueur, Fin, Portes)))

def choixlaby():
    """Menu de selection des cartes"""
    contenu = glob.glob(EMPLACEMENTCARTES)
    if not contenu:
        print(MESSAGEERREURDOSSIER.format(EMPLACEMENTCARTES))
        exit()
    chemin = EMPLACEMENTCARTES.find("*")
    effaceEtAffiche(MESSAGECHOIXCARTE)
    for i, carte in enumerate(contenu):
        print("{0} - {1}".format(i+1, carte[chemin:-4].capitalize()))
    print("Q - Quitter")
    i=0
    while i <3:
        choix = input()
        if choix.upper() == "Q":
            exit()
        try:
            choix = int(choix)
            carte = contenu[choix-1]
            essai = True
        except:
            essai = False
        if os.path.exists(carte) and essai:
            return carte
            break
        else:
            i +=1
            print(MESSAGEERREURCHOIXCARTE)
    print(MESSAGEECHECCHOIXCARTE)
    exit()

def labyload(fichier):
    """Charge la carte selectionnée"""
    if os.path.exists(fichier):
        with open(fichier, "r") as carte:
            return carte.read()

def labymap(carte):
    """Converti la carte (str) en tableau à 2 dimensions
    et liste les obstacles, point de départ et fin"""
    lines = carte.split("\n")
    Portes = []
    LabyMap = []
    for i, line in enumerate(lines):
        LabyMap.append([])
        for j, letter in enumerate(line):
            LabyMap[i].append(letter)
            if letter is LETTREJOUEUR:
                PosJoueur = [i,j]
            elif letter is LETTREFIN:
                Fin = [i,j]
            elif letter is LETTREPORTE:
                Portes.append((i,j))
    try:
        return(LabyMap, PosJoueur, Fin, Portes)
    except:
        return labymap(CARTEDEFAUT)

def playermove(LabyMap, PosJoueur, Fin, Portes, LabyOn):
    """Fait bouger le joueur"""
    noinput = True
    print(MESSAGEDEMANDEMOUVEMENT)
    while noinput:
        x=capturesaisie()
        print(x)
        if x == CTRL_C:
            exit()
        if x == ECHAP_CARAC:
            orig_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin)
            y=sys.stdin.read(2)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
            x = x+y
        if x==FLECHE_HAUT:
            axe, sens, noinput = 0,-1, False
        elif x==FLECHE_BAS:
            axe, sens, noinput = 0, 1, False
        elif x==FLECHE_DROITE:
            axe, sens, noinput = 1, 1, False
        elif x==FLECHE_GAUCHE:
            axe, sens, noinput = 1,-1, False
        elif x.lower()=='q':
            axe, sens = 0, 0
            noinput =  LabyOn = False

    TestPos = list(PosJoueur)
    TestPos[axe] += sens

    if LabyMap[TestPos[0]][TestPos[1]] \
    in (LETTRECOULOIR, LETTREPORTE, LETTREFIN):
        if tuple(PosJoueur) in Portes:
            LabyMap[PosJoueur[0]][PosJoueur[1]] = LETTREPORTE
        else:
            LabyMap[PosJoueur[0]][PosJoueur[1]] = LETTRECOULOIR
        PosJoueur = list(TestPos)
        LabyMap[PosJoueur[0]][PosJoueur[1]] = LETTREJOUEUR
        afficheLaby(LabyMap)
        if PosJoueur == Fin:
            LabyOn = False
            os.remove(FICHIERDESAUVEGARDE)
            print(MESSAGEREUSSITELABY)
            capturesaisie()
            return (LabyMap, PosJoueur, Fin, Portes, LabyOn)

    if LabyOn:
        sauvegarde(LabyMap, PosJoueur, Fin, Portes)
    return (LabyMap, PosJoueur, Fin, Portes, LabyOn)

def capturesaisie():
    """Renvoie la touche de clavier pressée"""
    if SYSTEME_D_EXPLOITATION == 'nt':
        print("Je ne sais pas encore faire ça")
    else:
        orig_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        saisie=sys.stdin.read(1)[0]
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
    return saisie
