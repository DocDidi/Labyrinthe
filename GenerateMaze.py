#! /usr/bin/env python3
# coding: utf-8

import random

class Cell:
    def __init__(self, i, j, valeur):
        self.i = i
        self.j = j
        self.valeur = valeur
        self.up = True
        self.down = True
        self.left = True
        self.right = True
    def __str__(self):
        # chaine = ""
        # if self.up: chaine+="U"
        # if self.down: chaine+="D"
        # if self.left: chaine+="L"
        # if self.right: chaine+="R"
        # return chaine
        return str(self.i)+str(self.j)+str(self.valeur)
    def __repr__(self):
        chaine = ""
        if self.up: chaine+="U"
        if self.down: chaine+="D"
        if self.left: chaine+="L"
        if self.right: chaine+="R"
        return chaine
        # return str(self.i)+str(self.j)+str(self.valeur)
    def testMur(self, Grid):
        x=random.randint(1,4)
        if x == 1: # Up
            if self.i-1 > 0:
                cible = Grid[self.i-1][self.j]
                if cible.valeur != self.valeur:
                    NouvelleValeur = min(cible.valeur, self.valeur)
                    AncienneValeur = max(cible.valeur, self.valeur)
                    modifValeurs(AncienneValeur,NouvelleValeur,Grid)
                    self.up = False
                    # cible.down = False
        if x == 2: # Down
            try:
                cible = Grid[self.i+1][self.j]
                if cible.valeur != self.valeur:
                    NouvelleValeur = min(cible.valeur, self.valeur)
                    AncienneValeur = max(cible.valeur, self.valeur)
                    modifValeurs(AncienneValeur,NouvelleValeur,Grid)
                    self.down = False
                    # cible.up = False
            except:
                pass
        if x == 3: # Left
            if self.j-1 > 0:
                cible = Grid[self.i][self.j-1]
                if cible.valeur != self.valeur:
                    NouvelleValeur = min(cible.valeur, self.valeur)
                    AncienneValeur = max(cible.valeur, self.valeur)
                    modifValeurs(AncienneValeur,NouvelleValeur,Grid)
                    self.left = False
                    # cible.right = False
        if x == 4: # Right
            try:
                cible = Grid[self.i][self.j+1]
                if cible.valeur != self.valeur:
                    NouvelleValeur = min(cible.valeur, self.valeur)
                    AncienneValeur = max(cible.valeur, self.valeur)
                    modifValeurs(AncienneValeur,NouvelleValeur,Grid)
                    self.right = False
                    # cible.left = False
            except:
                pass

def modifValeurs(Ancienne, Nouvelle, Grid):
    for i in Grid:
        for j in i:
            if j.valeur == Ancienne:
                j.valeur = Nouvelle
                # input("OK!")

def roundToSupOdd(x):
    if x % 2 == 1:
        return x
    else:
        return x + 1
def roundToInfEven(x):
    if x % 2 == 0:
        return x
    else:
        return x -1

def canevas(w,h):
    w = roundToSupOdd(w)
    h = roundToSupOdd(h)
    canevas = []
    for i in range(h):
        canevas.append([])
        for j in range(w):
            canevas[i].append("X")
    return canevas

def affCarte(carte):
    chainecanevas=""
    for line in carte:
        for letter in line:
            chainecanevas += letter
        chainecanevas += "\n"
    print(chainecanevas[:-1])


def grid(w, h):
    valeur = 0
    w = w//2
    h = h//2
    Grid = []
    for i in range(h):
        Grid.append([])
        for j in range(w):
            Grid[i].append(Cell(i,j,valeur))
            valeur += 1
    return Grid

def makeMaze(w,h):
    Grid = grid(w,h)
    carte = canevas(w,h)
    while True:
        ActiveCell = random.choice(random.choice(Grid))
        ActiveCell.testMur(Grid)
        Test = 0
        for i in Grid:
            for j in i:
                Test += j.valeur
        if Test == 0:
            break
    for i, line in enumerate(Grid):
        for j, item in enumerate(line):
            carte[i*2+1][j*2+1] = " "
            if item.up == False:
                carte[i*2][j*2+1] = " "

            if item.down == False:
                carte[i*2+2][j*2+1] = " "

            if item.left == False:
                carte[i*2+1][j*2] = " "

            if item.right == False:
                carte[i*2+1][j*2+2] = " "
    affCarte(carte)

makeMaze(16,16)
