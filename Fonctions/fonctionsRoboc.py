#! /usr/bin/env python3
# coding: utf-8

import os, glob, pickle, sys, termios, tty
from Fonctions.var import *
from Fonctions.Joueur import *
from Fonctions.Mur import *
from Fonctions.Porte import *
from Fonctions.Couloir import *
from Fonctions.GenerateMaze import *

def effaceEtAffiche(*valeur):
    """Efface l'écran et positionne le curseur en haut a gauche.
    Peut prendre en entrée une chaine de caracteres à afficher"""
    print(EFFACE_ECRAN)
    if valeur == ():
        print(RESET_CURSEUR, end = "")
    else:
        print(RESET_CURSEUR + WHITE_TEXT + valeur[0])

def verifTailleConsole(Hauteur, Largeur):
    """Demande a l'utilisateur d'agrandir sa console si besoin."""
    HAUTEURECRANCORRECT = True
    LARGEURECRANCORRECT = True
    rows, columns = os.popen('stty size', 'r').read().split()
    while int(rows) < Hauteur + 3:
        HAUTEURECRANCORRECT = False
        rows, columns = os.popen('stty size', 'r').read().split()
        effaceEtAffiche(MESSAGEHAUTEURECRANINCORRECT)
    if HAUTEURECRANCORRECT == False:
        effaceEtAffiche(MESSAGEECRANCORRECT)
        input()
    while int(columns) < Largeur:
        LARGEURECRANCORRECT = False
        rows, columns = os.popen('stty size', 'r').read().split()
        effaceEtAffiche(MESSAGELARGEURECRANINCORRECT)
    if LARGEURECRANCORRECT == False:
        effaceEtAffiche(MESSAGEECRANCORRECT)
        input()

def afficheLaby(Joueur, Props, Hauteur, Largeur):
    """Affiche le labyrinthe."""
    carte = ""
    for item in Props:
        carte = carte + str(item)
    effaceEtAffiche(carte)
    print(Joueur)
    print(WHITE_TEXT + MESSAGEDEMANDEMOUVEMENT.format(Hauteur + 2))

def sauvegardePartie(Joueur, Props, Hauteur, Largeur, laby):
    """Sauvegarde la partie"""
    with open(FICHIERDESAUVEGARDE, "wb") as Sauvegarde:
        Sauvegarde.write(pickle.dumps((Joueur, Props, Hauteur, Largeur, laby)))

def repriseSauvegarde():
    """Propose de reprendre la partie précedente
    Renvoie un Tuple contenant les Joueur, Props, Hauteur, Largeur
    qui étaient dans le fichier"""
    if os.path.exists(FICHIERDESAUVEGARDE):
        print(WHITE_TEXT + MESSAGEREPRISESAUVEGARDE)
        choix = capturesaisie(1)
        if choix.lower() == "o":
            with open(FICHIERDESAUVEGARDE, "rb") as Sauvegarde:
                PartieEnCours = pickle.loads(Sauvegarde.read())
        else:
            os.remove(FICHIERDESAUVEGARDE)
            PartieEnCours = False
    else:
        PartieEnCours = False
    return (PartieEnCours)

def choixlaby(selected = 0):
    """Menu de selection des cartes.
    Renvoie le nom du fichier choisi ou la carte aléatoire."""
    contenu = glob.glob(CHARGEMENTCARTES)
    indice = 0
    if not contenu:
        print(WHITE_TEXT = MESSAGEERREURDOSSIER.format(CHARGEMENTCARTES))
        exit()
    chemin = CHARGEMENTCARTES.find("*")
    chosen = False
    while not chosen:
        choix =[MESSAGECARTEPREDEFINIE+contenu[indice][chemin:-4].capitalize()]\
        + [MESSAGECHOIXCARTEALEATOIREPETITE, MESSAGECHOIXCARTEALEATOIREGRANDE,\
        MESSAGECHOIXCARTEALEATOIREECRAN, MESSAGECHOIXQUITTER]
        effaceEtAffiche(WHITE_TEXT + MESSAGECHOIXCARTE)
        for i, carte in enumerate(choix):
            if i == selected:
                if os.path.exists(carte):
                    print(BLACK_ON_WHITE + carte[chemin:-4].capitalize())
                else:
                    print(BLACK_ON_WHITE + carte + WHITE_TEXT)
            else:
                if os.path.exists(carte):
                    print(WHITE_TEXT + carte[chemin:-4].capitalize())
                else:
                    print(WHITE_TEXT + carte)
        noinput = True
        while noinput:
            x=capturesaisie(1)
            if x == CTRL_C:
                exit()
            elif ord(x) == 13:
                chosen = choix[selected]
                noinput = False
            elif x == ECHAP_CARAC:
                y = capturesaisie(2)
                x = x+y
            elif x.lower()=='q':
                exit()
            if x==FLECHE_BAS:
                if selected < (len(choix)-1):
                    selected += 1
                noinput = False
            elif x==FLECHE_HAUT:
                if selected > 0:
                    selected -= 1
                noinput = False
            elif x==FLECHE_GAUCHE and indice > 0:
                indice -= 1
                noinput = False
            elif x==FLECHE_DROITE and indice < len(contenu)-1:
                indice += 1
                noinput = False
    if chosen == MESSAGECARTEPREDEFINIE+contenu[indice][chemin:-4].capitalize():
        chosen = contenu[indice]
        if os.path.exists(chosen):
            with open(chosen, "r") as carte:
                return carte.read(), selected
    elif chosen == MESSAGECHOIXCARTEALEATOIREPETITE:
        carte = makeMaze(LARGEURPETITE,HAUTEURPETITE)
        return carte, selected
    elif chosen == MESSAGECHOIXCARTEALEATOIREGRANDE:
        carte = makeMaze(LARGEURGRANDE,HAUTEURGRANDE)
        return carte, selected
    elif chosen == MESSAGECHOIXCARTEALEATOIREECRAN:
        rows, columns = os.popen('stty size', 'r').read().split()
        carte = makeMaze(int(columns)-1,int(rows)-4)
        return carte, selected
    elif chosen == MESSAGECHOIXQUITTER:
        exit()
    else:
        print(WHITE_TEXT + MESSAGEERREURCHOIXCARTE)
        print(chosen)
        exit()

def labymap(carte):
    """Extrait les données du jeu de la carte (str)
    Renvoie Joueur, Props, Hauteur, Largeur"""
    lines = carte.split("\n")
    Props = []
    Murs = []
    Portes = []
    Couloirs = []
    for i, line in enumerate(lines):
        for j, letter in enumerate(line):
            if letter is LETTREJOUEUR:
                Joueur = Personnage(i,j)
                Props.append(Couloir(i,j))
            elif letter is LETTREFIN:
                Props.append(Porte(i,j,fin = True))
            elif letter is LETTREPORTE:
                Props.append(Porte(i,j))
            elif letter is LETTREMURS:
                Props.append(Mur(i,j))
            else:
                Props.append(Couloir(i,j))

    try:
        return(Joueur, Props, i, j)
    except:
        return labymap(CARTEDEFAUT)

def playermove(Joueur, Props, LabyOn, Hauteur):
    """Fait bouger le joueur
    Renvoie LabyOn == True si le jeu continue."""
    noinput = True
    TestPosJoueur = [Joueur.y, Joueur.x]
    cheatcode = 0
    while noinput:
        x=capturesaisie(1)
        if x == CTRL_C:
            exit()
        elif x.lower()=='q':
            noinput =  LabyOn = False
        elif x.lower()=='d':
            cheatcode = 1
        elif x.lower()=='o' and cheatcode == 1:
            cheatcode = 2
        elif x.lower()=='c' and cheatcode == 2:
            for item in Props:
                item.revealed = True
                noinput = False
        elif x == ECHAP_CARAC:
            y = capturesaisie(2)
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

    bloc = False
    for item in Props:
        if (TestPosJoueur[1], TestPosJoueur[0]) == (item.x, item.y)\
        and item.bloc == True:
            bloc = True
    if bloc == False:
        Joueur.x = TestPosJoueur[1]
        Joueur.y = TestPosJoueur[0]

    return (LabyOn)

def capturesaisie(nbl):
    """Renvoie la ou les touches de clavier pressées.
    Prend le nombre de touches à renvoyer"""
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin)
    saisie=sys.stdin.read(nbl)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
    return saisie

def isLit(sujet, Joueur):
    """Calcule si l'objet est éclairé"""
    if ((-1 <= Joueur.x - sujet.x <= 1) and (-2 <= Joueur.y - sujet.y <= 2)) or\
    ((-2 <= Joueur.x - sujet.x <= 2) and (-1 <= Joueur.y - sujet.y <= 1)):
        sujet.revealed = True
        sujet.lit = True
    else:
        sujet.lit = False
    if Joueur.x == sujet.x and Joueur.y == sujet.y:
        sujet.visited = True

def brouillard(Joueur, Props):
    """Liste les choses à reveler et les passe a la fonction isLit"""
    for item in Props:
        isLit(item, Joueur)

def finishedMenu(laby, Hauteur, Temps):
    """Messages et menu de choix quand le labyrinthe est fini."""
    Temps = convTemps(Temps)
    # Temps = "{:.2f}".format(Temps)
    print(WHITE_TEXT+MESSAGEREUSSITELABY.format(Hauteur +1,Temps))
    noinput = True
    while noinput:
        x = capturesaisie(1)
        if x == CTRL_C:
            exit()
        elif x.lower() == "q":
            noinput = False
        elif x.lower() == "s":
            sauvegardeLaby(laby)
            noinput = False

def convTemps(Temps):
    minutes = int(Temps // 60)
    secondes = int(Temps % 60)
    heures = minutes // 60
    minutes == minutes % 60
    if secondes <= 1:
        motsec = "seconde"
    else:
        motsec = "secondes"
    if minutes <= 1:
        motmin = "minute"
    else:
        motmin = "minutes"
    if not minutes and not heures:
        return "{0} {1}".format(secondes,motsec)
    elif not heures:
        return "{0} {1}, {2} {3}".format(minutes,motmin, secondes,motsec)
    else:
        return "Plus d'une heure !"

def sauvegardeLaby(laby):
    """Sauvegarde le labyrinthe"""
    effaceEtAffiche()
    fichier = input(laby+MESSAGESAUVEGARDELABYRINTHE)
    fichier = EMPLACEMENTCARTES + fichier + FORMATCARTE
    print(type(laby))
    with open(fichier, "w") as Sauvegarde:
            Sauvegarde.write(laby)
