#! /usr/bin/env python3
# coding: utf-8

from fonctionsRoboc import *

from var import *

GameOn = True
PartieEnCours = repriseSauvegarde()
while GameOn:
    # Boucle du jeu
    if PartieEnCours:
        Joueur, Props, Hauteur, Largeur = PartieEnCours
        PartieEnCours = False
    else:
        fichier, hasard = choixlaby()
        if fichier:
            laby = labyload(fichier)
        if hasard:
            laby = hasard
        Joueur, Props, Hauteur, Largeur = labymap(laby)
    verifTailleConsole(Hauteur, Largeur)
    effaceEtAffiche()
    LabyOn = True
    while LabyOn:
        brouillard(Joueur, Props)
        afficheLaby(Joueur, Props, Hauteur, Largeur)
        # PosJoueur = Joueur.PosJoueur()
        for porte in Props:
            if porte.fin:
                if (Joueur.x, Joueur.y) == (porte.x, porte.y):
                    LabyOn = False
                    os.remove(FICHIERDESAUVEGARDE)
                    print(WHITE_TEXT + MESSAGEREUSSITELABY.format(Hauteur +2))
                    capturesaisie()
                    break
                else:
                    LabyOn = playermove(Joueur, Props, LabyOn, Hauteur)
                    sauvegarde(Joueur, Props, Hauteur, Largeur)
