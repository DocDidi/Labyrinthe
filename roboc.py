#! /usr/bin/env python3
# coding: utf-8

from fonctionsRoboc import *

from var import *

GameOn = True
PartieEnCours = repriseSauvegarde()
while GameOn:
    # Boucle du jeu
    if PartieEnCours:
        Joueur, Murs, Portes, Hauteur = PartieEnCours
        PartieEnCours = False
    else:
        fichier = choixlaby()
        laby = labyload(fichier)
        Joueur, Murs, Portes, Hauteur = labymap(laby)
        # input(Murs)

    LabyOn = True
    while LabyOn:
        brouillard(Joueur, Murs, Portes)
        afficheLaby(Joueur, Murs, Portes)
        PosJoueur = Joueur.PosJoueur()
        for porte in Portes:
            if porte.fin:
                if (Joueur.x, Joueur.y) == (porte.x, porte.y):
                    LabyOn = False
                    os.remove(FICHIERDESAUVEGARDE)
                    print(WHITE_TEXT + MESSAGEREUSSITELABY.format(Hauteur +2))
                    capturesaisie()
                    break
                else:
                    LabyOn = playermove(Joueur, Murs, LabyOn, Hauteur)
                    sauvegarde(Joueur, Murs, Portes, Hauteur)
