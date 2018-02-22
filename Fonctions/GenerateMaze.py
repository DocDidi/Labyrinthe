#! /usr/bin/env python3
# coding: utf-8

import random, os

if __name__ == '__main__':
    from Variables_Map_Building import *
else:
    from Fonctions.Variables_Map_Building import *
    
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
        str_dir = ""
        if self.up: str_dir+="U"
        if self.down: str_dir+="D"
        if self.left: str_dir+="L"
        if self.right: str_dir+="R"
        return str_dir

    def wall_test(self, grid):
        """Choisi une direction au hasard et casse le mur si c'est possible"""
        x=random.randint(1,4)
        if x == 1: # Up
            if self.i-1 > 0:
                target_cell = grid[self.i-1][self.j]
                if target_cell.index_value != self.index_value:
                    change_index(target_cell.index_value,self.index_value,grid)
                    self.up = False
        if x == 2: # Down
            try:
                target_cell = grid[self.i+1][self.j]
                if target_cell.index_value != self.index_value:
                    change_index(target_cell.index_value,self.index_value,grid)
                    self.down = False
            except:
                pass
        if x == 3: # Left
            if self.j-1 > 0:
                target_cell = grid[self.i][self.j-1]
                if target_cell.index_value != self.index_value:
                    change_index(target_cell.index_value,self.index_value,grid)
                    self.left = False
        if x == 4: # Right
            try:
                target_cell = grid[self.i][self.j+1]
                if target_cell.index_value != self.index_value:
                    change_index(target_cell.index_value,self.index_value,grid)
                    self.right = False
            except:
                pass

def change_index(a, b, grid):
    """Modifie les index après le cassage d'un mur"""
    for i in grid:
        for j in i:
            if j.index_value == max(a, b):
                j.index_value = min(a, b)

def round_to_sup_odd(x):
    """Arrondi au chiffre impair supérieur"""
    if x % 2 == 1:
        return x
    else:
        return x + 1

def groundwork(w,h):
    """Prépare un canevas de la bonne taille pour y graver la carte"""
    w = round_to_sup_odd(w)
    h = round_to_sup_odd(h)
    groundwork = []
    for i in range(h):
        groundwork.append([])
        for j in range(w):
            groundwork[i].append(LETTER_WALL)
    return groundwork

def make_str_from_2d_array(maze_map):
    """Converti la carte (liste) en chaine de caracteres"""
    groundwork_str=""
    for line in maze_map:
        for letter in line:
            groundwork_str += letter
        groundwork_str += "\n"
    return groundwork_str

def make_grid(w, h):
    """Défini la grid de cells"""
    index_value = 0
    w = w//2
    h = h//2
    new_grid = []
    for i in range(h):
        new_grid.append([])
        for j in range(w):
            new_grid[i].append(Cell(i,j,index_value))
            index_value += 1
    return new_grid

def delete_isolated_wall(maze_map):
    """Supprime les murs isolés"""
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

def make_room(maze_map):
    """Ajoute une ou plusieurs salles dans le labyrinthe."""
    total_cells = len(maze_map)*len(maze_map[1])
    key_placed = False
    for i in range (total_cells//40):
        a = random.randint(1, ((len(maze_map)//2))-1)*2
        b = random.randint(1, ((len(maze_map[0])//2))-1)*2
        maze_map[a-1][b] = LETTER_CORRIDOR
        maze_map[a+1][b] = LETTER_CORRIDOR
        if i%3 == 0:
            maze_map[a][b-1] = LETTER_CORRIDOR
            maze_map[a][b+1] = LETTER_CORRIDOR
            if not key_placed:
                maze_map[a][b]=LETTER_KEY
                key_placed = True

    delete_isolated_wall(maze_map)

def find_eligible_exit(maze_map,corner):
    """Retourne une liste d'emplacement pour la sortie"""
    eligible_exits = []
    map_width = len(maze_map[0]) - 1
    map_height = len(maze_map) - 1
    if corner == "NW":
        for i in range(1, map_width//2):
            if maze_map[1][i] != LETTER_WALL:
                eligible_exits.append((0,i))
        for j in range(1, map_height//2):
            if maze_map[j][1] != LETTER_WALL:
                eligible_exits.append((j,0))
        return eligible_exits
    if corner == "NE":
        for i in range(map_width//2, map_width):
            if maze_map[1][i] != LETTER_WALL:
                eligible_exits.append((0,i))
        for j in range(1, map_height//2):
            if maze_map[j][map_width-1] != LETTER_WALL:
                eligible_exits.append((j,map_width))
        return eligible_exits
    if corner == "SW":
        for i in range(1, map_width//2):
            if maze_map[map_height-1][i] != LETTER_WALL:
                eligible_exits.append((map_height,i))
        for j in range(map_height//2, map_height):
            if maze_map[j][1] != LETTER_WALL:
                eligible_exits.append((j,0))
        return eligible_exits
    if corner == "SE":
        for i in range(map_width//2, map_width):
            if maze_map[map_height-1][i] != LETTER_WALL:
                eligible_exits.append((map_height,i))
        for j in range(map_height//2, map_height):
            if maze_map[j][map_width-1] != LETTER_WALL:
                eligible_exits.append((j,map_width))
        return eligible_exits


def make_entrance_and_exit(maze_map, number_of_players):
    """Place l'entrée et la sortie sur la carte"""
    locations = [ "NW", "NE", "SW", "SE"]
    for i in range(number_of_players):
        position_start = locations.pop(random.randint(0, len(locations)-1))
        if position_start == "NW":
            maze_map[1][1] = LETTER_PLAYER[i]
        elif position_start == "NE":
            maze_map[1][len(maze_map[1])-2] = LETTER_PLAYER[i]
        elif position_start == "SW":
            maze_map[len(maze_map)-2][1] = LETTER_PLAYER[i]
        elif position_start == "SE":
            maze_map[len(maze_map)-2][len(maze_map[1])-2] = LETTER_PLAYER[i]
    corner_end = locations.pop(random.randint(0, len(locations)-1))
    eligible_exits = find_eligible_exit(maze_map, corner_end)
    exit_location = eligible_exits.pop(random.randint(0, len(eligible_exits)-1))
    maze_map[exit_location[0]][exit_location[1]] = LETTER_END

def add_doors(maze_map):
    """Ajoute des portes sur la carte"""
    maze_map_old = []
    while maze_map != maze_map_old:
        maze_map_old = list(maze_map)
        for x in range(2,len(maze_map)-2):
            for y in range(2,len(maze_map[0])-2):
                if maze_map[x][y] == LETTER_WALL:
                    empty_spaces = []
                    if maze_map[x][y-1] == LETTER_CORRIDOR:
                        empty_spaces.append("W")
                    if maze_map[x][y+1] == LETTER_CORRIDOR:
                        empty_spaces.append("E")
                    if maze_map[x-1][y] == LETTER_CORRIDOR:
                        empty_spaces.append("N")
                    if maze_map[x+1][y] == LETTER_CORRIDOR:
                        empty_spaces.append("S")
                    if len(empty_spaces) == 3:
                        door_added = False
                        while not door_added:
                            if len(empty_spaces) == 0:
                                maze_map[x][y] = LETTER_CORRIDOR
                                maze_map[x-1][y] = LETTER_CORRIDOR
                                maze_map[x+1][y] = LETTER_CORRIDOR
                                maze_map[x][y-1] = LETTER_CORRIDOR
                                maze_map[x][y+1] = LETTER_CORRIDOR
                                delete_isolated_wall(maze_map)
                                break
                            door_try = empty_spaces\
                            .pop(random.randint(0, len(empty_spaces)-1))
                            if door_try == "W" and\
                            maze_map[x][y-2] == LETTER_WALL:
                                maze_map[x][y-1] = LETTER_DOOR
                                door_added = True
                            if door_try == "E" and\
                            maze_map[x][y+2] == LETTER_WALL:
                                maze_map[x][y+1] = LETTER_DOOR
                                door_added = True
                            if door_try == "N" and\
                            maze_map[x-2][y] == LETTER_WALL:
                                maze_map[x-1][y] = LETTER_DOOR
                                door_added = True
                            if door_try == "S" and\
                            maze_map[x+2][y] == LETTER_WALL:
                                maze_map[x+1][y] = LETTER_DOOR
                                door_added = True

def make_maze(w,h, number_of_players = 1):
    """Fonction principale.
    Construit un labyrinthe à la taille demandée."""
    grid = make_grid(w,h)
    maze_map = groundwork(w,h)
    while True:
        cell_active = random.choice(random.choice(grid))
        cell_active.wall_test(grid)
        test_finished = 0
        for i in grid:
            for j in i:
                test_finished += j.index_value
        if test_finished == 0:
            break
    for i, line in enumerate(grid):
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
    make_room(maze_map)
    make_entrance_and_exit(maze_map, number_of_players)
    add_doors(maze_map)
    map_finished = make_str_from_2d_array(maze_map)
    return map_finished


if __name__ == '__main__':
    # rows, columns = os.popen('stty size', 'r').read().split()
    # maze_map = make_maze(int(columns),int(rows)-1)
    maze_map = make_maze(54,27,number_of_players = 2)
    print(maze_map)
