#! /usr/bin/env python3
# coding: utf-8

import random, os
from var import *

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
        return str(self.i)+str(self.j)+str(self.valeur)
    def __repr__(self):
        chaine = ""
        if self.up: chaine+="U"
        if self.down: chaine+="D"
        if self.left: chaine+="L"
        if self.right: chaine+="R"
        return chaine
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
        if x == 2: # Down
            try:
                cible = Grid[self.i+1][self.j]
                if cible.valeur != self.valeur:
                    NouvelleValeur = min(cible.valeur, self.valeur)
                    AncienneValeur = max(cible.valeur, self.valeur)
                    modifValeurs(AncienneValeur,NouvelleValeur,Grid)
                    self.down = False
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
        if x == 4: # Right
            try:
                cible = Grid[self.i][self.j+1]
                if cible.valeur != self.valeur:
                    NouvelleValeur = min(cible.valeur, self.valeur)
                    AncienneValeur = max(cible.valeur, self.valeur)
                    modifValeurs(AncienneValeur,NouvelleValeur,Grid)
                    self.right = False
            except:
                pass

def modifValeurs(Ancienne, Nouvelle, Grid):
    for i in Grid:
        for j in i:
            if j.valeur == Ancienne:
                j.valeur = Nouvelle

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
            canevas[i].append(LETTREMURS)
    return canevas

def convCarteStr(carte):
    chainecanevas=""
    for line in carte:
        for letter in line:
            chainecanevas += letter
        chainecanevas += "\n"
    return chainecanevas


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

def makeEntranceAndExit(carte):
    locations = [ "NO", "NE", "SO", "SE"]
    ChoixD = locations.pop(random.randint(0, len(locations)-1))
    # print(ChoixD, locations)
    if ChoixD == "NO":
        carte[1][1] = LETTREJOUEUR
    elif ChoixD == "NE":
        carte[1][len(carte[1])-2] = LETTREJOUEUR
    elif ChoixD == "SO":
        carte[len(carte)-2][1] = LETTREJOUEUR
    elif ChoixD == "SE":
        carte[len(carte)-2][len(carte[1])-2] = LETTREJOUEUR
    ChoixA = locations.pop(random.randint(0, len(locations)-1))
    # print(ChoixA, locations)
    if ChoixA == "NO":
        carte[0][1] = LETTREFIN
    elif ChoixA == "NE":
        carte[0][len(carte[1])-2] = LETTREFIN
    elif ChoixA == "SO":
        carte[len(carte)-1][1] = LETTREFIN
    elif ChoixA == "SE":
        carte[len(carte)-1][len(carte[1])-2] = LETTREFIN

def addDoors(carte):
    for i in range((len(carte)*len(carte[1]))//5):
        x = random.randint(0, len(carte[1])-1)
        y = random.randint(0, len(carte)-1)
        if carte[y][x] == LETTRECOULOIR:
            if carte[y][x-1] == LETTREMURS and carte[y][x+1] == LETTREMURS and\
            carte[y-1][x] == LETTRECOULOIR and carte[y+1][x] == LETTRECOULOIR:
                carte[y][x] = LETTREPORTE

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
            carte[i*2+1][j*2+1] = LETTRECOULOIR
            if item.up == False:
                carte[i*2][j*2+1] = LETTRECOULOIR

            if item.down == False:
                carte[i*2+2][j*2+1] = LETTRECOULOIR

            if item.left == False:
                carte[i*2+1][j*2] = LETTRECOULOIR

            if item.right == False:
                carte[i*2+1][j*2+2] = LETTRECOULOIR
    makeEntranceAndExit(carte)
    addDoors(carte)
    CarteStr = convCarteStr(carte)
    return CarteStr


if __name__ == '__main__':
    rows, columns = os.popen('stty size', 'r').read().split()
    carte = makeMaze(int(columns),int(rows)-1)
    print(carte)
