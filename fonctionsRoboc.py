#! /usr/bin/env python3
# coding: utf-8

import glob, pickle, sys, time
from var import *
from Joueur import *
from Mur import *
from Porte import *

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


def afficheLaby(Joueur, Murs, Portes):
    """Affiche le labyrinthe"""
    effaceEtAffiche()
    for mur in Murs:
        if mur.revealed == True:
            print(mur)
    for porte in Portes:
        if porte.revealed == True:
            print(porte)
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

def sauvegarde(Joueur, Murs, Portes, Hauteur):
    """Sauvegarde la partie"""
    with open(FICHIERDESAUVEGARDE, "wb") as Sauvegarde:
        Sauvegarde.write(pickle.dumps((Joueur, Murs, Portes, Hauteur)))

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
    """Converti la carte (str) en données du jeu"""
    lines = carte.split("\n")
    Portes = []
    LabyMap = []
    Murs = []
    for i, line in enumerate(lines):
        LabyMap.append([])
        for j, letter in enumerate(line):
            LabyMap[i].append(letter)
            if letter is LETTREJOUEUR:
                Joueur = Personnage(i,j)
            elif letter is LETTREFIN:
                Portes.append(Porte(i,j,fin = True))
            elif letter is LETTREPORTE:
                Portes.append(Porte(i,j))
            elif letter is LETTREMURS:
                Murs.append(Mur(i,j))
    try:
        return(Joueur, Murs, Portes, len(lines))
    except:
        return labymap(CARTEDEFAUT)

def playermove(Joueur, Murs, LabyOn, Hauteur):
    """Fait bouger le joueur"""
    noinput = True
    print(WHITE_TEXT + MESSAGEDEMANDEMOUVEMENT.format(Hauteur + 2))
    TestPosJoueur = [Joueur.y, Joueur.x]
    while noinput:
        x=capturesaisie()
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
        elif x==FLECHE_BAS:
            TestPosJoueur = [Joueur.y+1,Joueur.x]
            noinput = False
        elif x==FLECHE_DROITE:
            TestPosJoueur = [Joueur.y,Joueur.x+1]
            noinput = False
        elif x==FLECHE_GAUCHE:
            TestPosJoueur = [Joueur.y,Joueur.x-1]
            noinput = False
        elif x.lower()=='q':
            noinput =  LabyOn = False

    bloc = False

    for mur in Murs:
        if (TestPosJoueur[1], TestPosJoueur[0]) == (mur.x, mur.y):
            bloc = True

    if bloc == False:
        Joueur.x = TestPosJoueur[1]
        Joueur.y = TestPosJoueur[0]

    return (LabyOn)

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

def brouillard(Joueur, Murs, Portes):
    """Modifie l'attribut revealed des murs"""
    for mur in Murs:
        if (-2 <= Joueur.x - mur.x <= 2) and (-2 <= Joueur.y - mur.y <= 2):
            mur.revealed = True
    for porte in Portes:
        if (-2 <= Joueur.x - porte.x <= 2) and (-2 <= Joueur.y - porte.y <= 2):
            porte.revealed = True
