#! /usr/bin/env python3
# coding: utf-8

from fonctionsRoboc import *

from var import *

if SYSTEME_D_EXPLOITATION == 'nt':
    print(MESSAGEINCOMPATIBILITESYSTEME)
    exit()

GameOn = True
PartieEnCours = repriseSauvegarde()

while GameOn:
    if PartieEnCours:
        Joueur, Props, Hauteur, Largeur = PartieEnCours
        PartieEnCours = False
    else:
        laby = choixlaby()
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
                    print(WHITE_TEXT + MESSAGEREUSSITELABY.format(Hauteur +2))
                    capturesaisie(1)
                    break
                else:
                    LabyOn = playermove(Joueur, Props, LabyOn, Hauteur)
                    sauvegarde(Joueur, Props, Hauteur, Largeur)
