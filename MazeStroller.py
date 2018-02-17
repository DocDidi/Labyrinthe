#! /usr/bin/env python3
# coding: utf-8

from Fonctions.fonctionsRoboc import *

from Fonctions.var import *

if SYSTEME_D_EXPLOITATION == 'nt':
    print(MESSAGEINCOMPATIBILITESYSTEME)
    exit()

GameOn = True
PartieEnCours = repriseSauvegarde()
selected = 0

while GameOn:
    if PartieEnCours:
        Joueur, Props, Hauteur, Largeur = PartieEnCours
        PartieEnCours = False
    else:
        laby, selected = choixlaby(selected)
        Joueur, Props, Hauteur, Largeur = labymap(laby)
    verifTailleConsole(Hauteur, Largeur)
    effaceEtAffiche()
    LabyOn = True
    while LabyOn:
        brouillard(Joueur, Props)
        afficheLaby(Joueur, Props, Hauteur, Largeur)
        for porte in Props:
            if porte.fin:
                if (Joueur.x, Joueur.y) == (porte.x, porte.y):
                    LabyOn = False
                    os.remove(FICHIERDESAUVEGARDE)
                    for item in Props:
                        item.revealed = True
                    effaceEtAffiche()
                    afficheLaby(Joueur, Props, Hauteur, Largeur)
                    for item in Props:
                        try:
                            if item.visited:
                                print("{0}\033[{1};{2}H{3}".format\
                                (WHITE_TEXT,item.y+1,item.x+1,\
                                SYMBOLECOULOIRVISITE))
                        except:
                            pass
                    print(WHITE_TEXT + MESSAGEREUSSITELABY.format(Hauteur +2))
                    capturesaisie(1)
                    break
                else:
                    LabyOn = playermove(Joueur, Props, LabyOn, Hauteur)
                    sauvegarde(Joueur, Props, Hauteur, Largeur)
