#! /usr/bin/env python3
# coding: utf-8

import os, glob, pickle, sys, time
from var import *
from Joueur import *

def effaceEtAffiche(*valeur):
    """Efface l'écran et positionne le curseur en haut a gauche."""
    if SYSTEME_D_EXPLOITATION == 'nt':
        os.system('cls')
        if valeur:
            print(valeur[0])
    else:
        print(EFFACE_ECRAN)
        if valeur == ():
            print(RESET_CURSEUR, end = "")
        else:
            print(RESET_CURSEUR + WHITE_TEXT + valeur[0])


def afficheLaby(LabyMap, Joueur):
    """Affiche le labyrinthe"""
    tampon=""
    for line in LabyMap:
        for letter in line:
            if letter == LETTREMURS:
                tampon += YELLOW_TEXT + SYMBOLEMUR
            elif letter == LETTREPORTE:
                tampon += GREEN_TEXT + SYMBOLEPORTE
            elif letter == LETTREFIN:
                tampon += SYMBOLEFIN
            # elif letter == LETTREJOUEUR:
            #     tampon += CYAN_TEXT + SYMBOLEJOUEUR
            else:
                tampon += letter
        tampon += "\n"
    effaceEtAffiche(tampon)
    print(Joueur)

def repriseSauvegarde():
    """Propose de reprendre la partie précedente"""
    if os.path.exists(FICHIERDESAUVEGARDE):
        print(WHITE_TEXT + MESSAGEREPRISESAUVEGARDE)
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

def sauvegarde(LabyMap, Joueur, Fin, Portes):
    """Sauvegarde la partie"""
    with open(FICHIERDESAUVEGARDE, "wb") as Sauvegarde:
        Sauvegarde.write(pickle.dumps((LabyMap, Joueur, Fin, Portes)))

def choixlaby():
    """Menu de selection des cartes"""
    contenu = glob.glob(EMPLACEMENTCARTES)
    if not contenu:
        print(WHITE_TEXT = MESSAGEERREURDOSSIER.format(EMPLACEMENTCARTES))
        exit()
    chemin = EMPLACEMENTCARTES.find("*")
    effaceEtAffiche(MESSAGECHOIXCARTE)
    for i, carte in enumerate(contenu):
        print(WHITE_TEXT + "{0} - {1}"\
        .format(i+1, carte[chemin:-4].capitalize()))
    print(WHITE_TEXT + "Q - Quitter")
    i=0
    while i <3:
        choix = input()
        try:
            choix = choix.upper()
        except:
            pass
        if choix == "Q":
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
            print(WHITE_TEXT + MESSAGEERREURCHOIXCARTE)
    print(WHITE_TEXT + MESSAGEECHECCHOIXCARTE)
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
                # PosJoueur = [i,j]
                Joueur = Personnage(i,j)
            elif letter is LETTREFIN:
                Fin = [i,j]
            elif letter is LETTREPORTE:
                Portes.append((i,j))
    try:
        return(LabyMap, Joueur, Fin, Portes)
    except:
        return labymap(CARTEDEFAUT)

def playermove(LabyMap, Joueur, Fin, Portes, LabyOn):
    """Fait bouger le joueur"""
    noinput = True
    PosJoueur = Joueur.PosJoueur()
    print(WHITE_TEXT + MESSAGEDEMANDEMOUVEMENT.format(len(LabyMap)+2))
    TestPosJoueur = [Joueur.y, Joueur.x]
    while noinput:
        x=capturesaisie()
        # print(x)
        if x == CTRL_C:
            exit()
        if x == ECHAP_CARAC:
            import termios, tty
            orig_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin)
            y=sys.stdin.read(2)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
            x = x+y
        if x==FLECHE_HAUT:
            TestPosJoueur = [Joueur.y-1,Joueur.x]
            noinput = False
            # axe, sens, noinput = 0,-1, False
        elif x==FLECHE_BAS:
            TestPosJoueur = [Joueur.y+1,Joueur.x]
            noinput = False
            # axe, sens, noinput = 0, 1, False
        elif x==FLECHE_DROITE:
            TestPosJoueur = [Joueur.y,Joueur.x+1]
            noinput = False
            # axe, sens, noinput = 1, 1, False
        elif x==FLECHE_GAUCHE:
            TestPosJoueur = [Joueur.y,Joueur.x-1]
            noinput = False
            # axe, sens, noinput = 1,-1, False
        elif x.lower()=='q':
            # axe, sens = 0, 0
            noinput =  LabyOn = False
        elif x.lower()=='d':
            print(PosJoueur, Fin)

    # TestPos = list(PosJoueur)
    # TestPos[axe] += sens

    if LabyMap[TestPosJoueur[0]][TestPosJoueur[1]] \
    in (LETTRECOULOIR, LETTREPORTE, LETTREFIN, LETTREJOUEUR):
        # if Joueur.PosJoueur() in Portes:
        #     LabyMap[Joueur.y][Joueur.x] = LETTREPORTE
        # else:
        #     LabyMap[Joueur.y][Joueur.x] = LETTRECOULOIR
        Joueur.x = TestPosJoueur[1]
        Joueur.y = TestPosJoueur[0]
        # PosJoueur = list(TestPos)
        # LabyMap[Joueur.y][Joueur.x] = LETTREJOUEUR
        # afficheLaby(LabyMap, Joueur)
        PosJoueur = Joueur.PosJoueur()
        if PosJoueur == Fin:
            LabyOn = False
            os.remove(FICHIERDESAUVEGARDE)
            print(WHITE_TEXT + MESSAGEREUSSITELABY.format(len(LabyMap)+2))
            capturesaisie()
            return (LabyMap, Fin, Portes, LabyOn)

    if LabyOn:
        sauvegarde(LabyMap, Joueur, Fin, Portes)
    return (LabyMap, Fin, Portes, LabyOn)

def capturesaisie():
    """Renvoie la touche de clavier pressée"""
    if SYSTEME_D_EXPLOITATION == 'nt':
        import keyboard
        saisie = keyboard.read_hotkey()
        if saisie == "up":
            saisie = FLECHE_HAUT
        elif saisie == "down":
            saisie = FLECHE_BAS
        elif saisie == "right":
            saisie = FLECHE_DROITE
        elif saisie == "left":
            saisie = FLECHE_GAUCHE
        keyboard.clear_all_hotkeys()
        return saisie

    else:
        import termios, tty
        orig_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        saisie=sys.stdin.read(1)[0]
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
    return saisie
