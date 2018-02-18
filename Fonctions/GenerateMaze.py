#! /usr/bin/env python3
# coding: utf-8

import random, os
if __name__ == '__main__':
    from Var import *
else:
    from Fonctions.Var import *

class Cell:
    def __init__(self, i, j, index_value):
        self.i = i
        self.j = j
        self.index_value = index_value
        self.up = True
        self.down = True
        self.left = True
        self.right = True
    def __str__(self):
        return str(self.i)+str(self.j)+str(self.index_value)
    def __repr__(self):
        chaine = ""
        if self.up: chaine+="U"
        if self.down: chaine+="D"
        if self.left: chaine+="L"
        if self.right: chaine+="R"
        return chaine

    def testMur(self, Grid):
        """Choisi une direction au hasard et casse le mur si c'est possible"""
        x=random.randint(1,4)
        if x == 1: # Up
            if self.i-1 > 0:
                cible = Grid[self.i-1][self.j]
                if cible.index_value != self.index_value:
                    modifValeurs(cible.index_value,self.index_value,Grid)
                    self.up = False
        if x == 2: # Down
            try:
                cible = Grid[self.i+1][self.j]
                if cible.index_value != self.index_value:
                    modifValeurs(cible.index_value,self.index_value,Grid)
                    self.down = False
            except:
                pass
        if x == 3: # Left
            if self.j-1 > 0:
                cible = Grid[self.i][self.j-1]
                if cible.index_value != self.index_value:
                    modifValeurs(cible.index_value,self.index_value,Grid)
                    self.left = False
        if x == 4: # Right
            try:
                cible = Grid[self.i][self.j+1]
                if cible.index_value != self.index_value:
                    modifValeurs(cible.index_value,self.index_value,Grid)
                    self.right = False
            except:
                pass

def modifValeurs(a, b, Grid):
    """Modifie les index après le cassage d'un mur"""
    NouvelleValeur = min(a, b)
    AncienneValeur = max(a, b)
    for i in Grid:
        for j in i:
            if j.index_value == AncienneValeur:
                j.index_value = NouvelleValeur

def roundToSupOdd(x):
    """Arrondi au chiffre impair supérieur"""
    if x % 2 == 1:
        return x
    else:
        return x + 1

def canevas(w,h):
    """Prépare un canevas de la bonne taille pour y graver la carte"""
    w = roundToSupOdd(w)
    h = roundToSupOdd(h)
    canevas = []
    for i in range(h):
        canevas.append([])
        for j in range(w):
            canevas[i].append(LETTER_WALL)
    return canevas

def convCarteStr(maze_map):
    """Converti la carte (liste) en chaine de caracteres"""
    chainecanevas=""
    for line in maze_map:
        for letter in line:
            chainecanevas += letter
        chainecanevas += "\n"
    return chainecanevas


def grid(w, h):
    """Défini la Grid de cells"""
    index_value = 0
    w = w//2
    h = h//2
    Grid = []
    for i in range(h):
        Grid.append([])
        for j in range(w):
            Grid[i].append(Cell(i,j,index_value))
            index_value += 1
    return Grid

def makeRoom(maze_map):
    """Ajoute une ou plusieurs salles dans le labyrinthe."""
    Gridcount = len(maze_map)*len(maze_map[1])
    for i in range (Gridcount//150):
        creatingrooms = True
        a = random.randint(1, ((len(maze_map)//2))-1)*2
        b = random.randint(1, ((len(maze_map[0])//2))-1)*2
        # print(a,b)
        maze_map[a-1][b] = LETTER_CORRIDOR
        maze_map[a][b-1] = LETTER_CORRIDOR
        maze_map[a][b+1] = LETTER_CORRIDOR
        maze_map[a+1][b] = LETTER_CORRIDOR
    for x in range(len(maze_map)-1):
        for y in range(len(maze_map[0])-1):
            if maze_map[x][y] == LETTER_WALL:
                try:
                    if maze_map[x][y-1] == LETTER_CORRIDOR and \
                    maze_map[x][y+1] == LETTER_CORRIDOR and \
                    maze_map[x-1][y] == LETTER_CORRIDOR and \
                    maze_map[x+1][y] == LETTER_CORRIDOR:
                        maze_map[x][y] = LETTER_CORRIDOR
                except:
                    pass

def makeEntranceAndExit(maze_map):
    """Place l'entrée et la sortie sur la carte"""
    locations = [ "NO", "NE", "SO", "SE"]
    ChoixD = locations.pop(random.randint(0, len(locations)-1))
    # print(ChoixD, locations)
    if ChoixD == "NO":
        maze_map[1][1] = LETTER_PLAYER
    elif ChoixD == "NE":
        maze_map[1][len(maze_map[1])-2] = LETTER_PLAYER
    elif ChoixD == "SO":
        maze_map[len(maze_map)-2][1] = LETTER_PLAYER
    elif ChoixD == "SE":
        maze_map[len(maze_map)-2][len(maze_map[1])-2] = LETTER_PLAYER
    ChoixA = locations.pop(random.randint(0, len(locations)-1))
    # print(ChoixA, locations)
    if ChoixA == "NO":
        maze_map[0][1] = LETTER_END
    elif ChoixA == "NE":
        maze_map[0][len(maze_map[1])-2] = LETTER_END
    elif ChoixA == "SO":
        maze_map[len(maze_map)-1][1] = LETTER_END
    elif ChoixA == "SE":
        maze_map[len(maze_map)-1][len(maze_map[1])-2] = LETTER_END

def addDoors(maze_map):
    """Ajoute des portes sur la carte"""
    for i in range((len(maze_map)*len(maze_map[1]))//5):
        x = random.randint(0, len(maze_map[1])-1)
        y = random.randint(0, len(maze_map)-1)
        if maze_map[y][x] == LETTER_CORRIDOR:
            if maze_map[y][x-1] == LETTER_WALL\
            and maze_map[y][x+1] == LETTER_WALL\
            and maze_map[y-1][x] == LETTER_CORRIDOR\
            and maze_map[y+1][x] == LETTER_CORRIDOR:
                maze_map[y][x] = LETTER_DOOR

def makeMaze(w,h):
    """Fonction principale.
    Construit un labyrinthe à la taille demandée."""
    Grid = grid(w,h)
    maze_map = canevas(w,h)
    while True:
        ActiveCell = random.choice(random.choice(Grid))
        ActiveCell.testMur(Grid)
        Test = 0
        for i in Grid:
            for j in i:
                Test += j.index_value
        if Test == 0:
            break
    for i, line in enumerate(Grid):
        for j, item in enumerate(line):
            maze_map[i*2+1][j*2+1] = LETTER_CORRIDOR
            if item.up == False:
                maze_map[i*2][j*2+1] = LETTER_CORRIDOR

            if item.down == False:
                maze_map[i*2+2][j*2+1] = LETTER_CORRIDOR

            if item.left == False:
                maze_map[i*2+1][j*2] = LETTER_CORRIDOR

            if item.right == False:
                maze_map[i*2+1][j*2+2] = LETTER_CORRIDOR
    makeRoom(maze_map)
    makeEntranceAndExit(maze_map)
    addDoors(maze_map)
    CarteStr = convCarteStr(maze_map)
    return CarteStr


if __name__ == '__main__':
    # rows, columns = os.popen('stty size', 'r').read().split()
    # maze_map = makeMaze(int(columns),int(rows)-1)
    maze_map = makeMaze(54,27)
    print(maze_map)
