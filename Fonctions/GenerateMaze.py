#! /usr/bin/env python3
# coding: utf-8

import random


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
        self.visited = False
        self.dead_end = False

    def wall_test_Kruskal(self, grid, indexed_list):
        """Pick a random direction and break the wall if possible"""
        tries = ["Up","Down","Left","Right"]
        random.shuffle(tries)
        for x in tries:
            if x == "Up" and self.i-1 > 0:
                target_cell = grid[self.i-1][self.j]
                if target_cell.index_value != self.index_value:
                    self.change_index(target_cell.index_value,indexed_list)
                    self.up = False
            if x == "Down" and self.i+1 < len(grid)-1:
                target_cell = grid[self.i+1][self.j]
                if target_cell.index_value != self.index_value:
                    self.change_index(target_cell.index_value,indexed_list)
                    self.down = False
            if x == "Left" and self.j-1 > 0:
                target_cell = grid[self.i][self.j-1]
                if target_cell.index_value != self.index_value:
                    self.change_index(target_cell.index_value,indexed_list)
                    self.left = False
            if x == "Right" and self.j+1 < len(grid[0])-1:
                target_cell = grid[self.i][self.j+1]
                if target_cell.index_value != self.index_value:
                    self.change_index(target_cell.index_value,indexed_list)
                    self.right = False

    def wall_test_RB(self, grid):
        """Pick a random direction and break the wall if possible"""
        self.visited = True
        tries = []
        if self.i-1 >= 0 and not grid[self.i-1][self.j].visited:
            tries.append((grid[self.i-1][self.j],"Up"))
        if self.i+1 < len(grid) and not grid[self.i+1][self.j].visited:
            tries.append((grid[self.i+1][self.j],"Down"))
        if self.j-1 >= 0 and not grid[self.i][self.j-1].visited:
            tries.append((grid[self.i][self.j-1],"Left"))
        if self.j+1 < len(grid[0]) and not grid[self.i][self.j+1].visited:
            tries.append((grid[self.i][self.j+1],"Right"))
        if len(tries) != 0:
            main_cell, direction = random.choice(tries)
            if direction == "Up":
                self.up = False
            if direction == "Down":
                self.down = False
            if direction == "Left":
                self.left = False
            if direction == "Right":
                self.right = False
        else:
            main_cell = self
            self.dead_end = True

        return main_cell

    def change_index(self, a, indexed_list):
        """Modify the indexes after a wall broke"""
        value_low = min(a, self.index_value)
        value_high = max(a, self.index_value)
        for item in indexed_list[value_high]:
            item.index_value = value_low
            indexed_list[value_low].append(item)
        indexed_list[value_high] = []

def round_to_sup_odd(x):
    """Round a number to its superior odd"""
    if x % 2 == 1:
        return x
    else:
        return x + 1

def groundwork(w,h):
    """Prepare a canvas to carve the map"""
    w = round_to_sup_odd(w)
    h = round_to_sup_odd(h)
    groundwork = []
    for i in range(h):
        groundwork.append([])
        for j in range(w):
            groundwork[i].append(LETTER_WALL)
    return groundwork

def make_str_from_2d_array(maze_map):
    """Convert a list into a string"""
    groundwork_str=""
    for line in maze_map:
        for letter in line:
            groundwork_str += letter
        groundwork_str += "\n"
    return groundwork_str

def make_grid(w, h):
    """Make a grid of cells"""
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
    """Delete isolated walls"""
    for x in range(1, len(maze_map)-2):
        for y in range(1, len(maze_map[0])-2):
            if maze_map[x][y] == LETTER_WALL:
                if maze_map[x][y-1] == LETTER_CORRIDOR and \
                maze_map[x][y+1] == LETTER_CORRIDOR and \
                maze_map[x-1][y] == LETTER_CORRIDOR and \
                maze_map[x+1][y] == LETTER_CORRIDOR:
                    maze_map[x][y] = LETTER_CORRIDOR

def make_room(maze_map):
    """Add rooms in the maze"""
    number_of_rooms = (len(maze_map)*len(maze_map[1])) // 50
    if number_of_rooms == 0:
        number_of_rooms = 1
    key_placed = False
    eligible_spots = []
    if len(maze_map) > 3 and len(maze_map[0]) > 3:
        for i in range(2, len(maze_map) -1, 2):
            for j in range(2, len(maze_map[0]) -1, 2):
                eligible_spots.append((i,j))
        random.shuffle(eligible_spots)
        for i in range (number_of_rooms):
            spot = eligible_spots.pop(0)
            a = spot[0]
            b = spot[1]
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
    """Find locations for the exit"""
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
    """Place enter and exit on the map"""
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
    """Add doors on the map"""
    maze_map_old = []
    while maze_map != maze_map_old:
        maze_map_old = [x[:] for x in maze_map]
        for x in range(2,len(maze_map)-2):
            for y in range(2,len(maze_map[0])-2):
                if maze_map[x][y] == LETTER_WALL:
                    empty_spaces = []
                    if maze_map[x][y-1] in (LETTER_CORRIDOR):
                        empty_spaces.append("W")
                    if maze_map[x][y+1] in (LETTER_CORRIDOR):
                        empty_spaces.append("E")
                    if maze_map[x-1][y] in (LETTER_CORRIDOR):
                        empty_spaces.append("N")
                    if maze_map[x+1][y] in (LETTER_CORRIDOR):
                        empty_spaces.append("S")
                    if len(empty_spaces) == 3:
                        door_added = False
                        random.shuffle(empty_spaces)
                        for door_try in empty_spaces:
                            if door_try == "W" and\
                            maze_map[x][y-2] == LETTER_WALL:
                                maze_map[x][y-1] = LETTER_DOOR
                                door_added = True
                                break
                            elif door_try == "E" and\
                            maze_map[x][y+2] == LETTER_WALL:
                                maze_map[x][y+1] = LETTER_DOOR
                                door_added = True
                                break
                            elif door_try == "N" and\
                            maze_map[x-2][y] == LETTER_WALL:
                                maze_map[x-1][y] = LETTER_DOOR
                                door_added = True
                                break
                            elif door_try == "S" and\
                            maze_map[x+2][y] == LETTER_WALL:
                                maze_map[x+1][y] = LETTER_DOOR
                                door_added = True
                                break
                        if not door_added:
                            maze_map[x][y] = LETTER_CORRIDOR
                            maze_map[x-1][y] = LETTER_CORRIDOR
                            maze_map[x+1][y] = LETTER_CORRIDOR
                            maze_map[x][y-1] = LETTER_CORRIDOR
                            maze_map[x][y+1] = LETTER_CORRIDOR
                            delete_isolated_wall(maze_map)


def make_maze(w,h, number_of_players = 1):
    """Build a maze of the requested size"""
    grid = make_grid(w,h)
    maze_map = groundwork(w,h)
    type_of_maze = random.randint(1,2)
    if type_of_maze == 1:
        # Kruskal
        list_of_cells = []
        for line in grid:
            for item in line:
                list_of_cells.append(item)
        indexed_list = []
        for item in list_of_cells:
            new_list = [item]
            indexed_list.append(new_list)
        random.shuffle(list_of_cells)
        for cell_active in list_of_cells:
            cell_active.wall_test_Kruskal(grid, indexed_list)
    elif type_of_maze == 2:
        # recursive bactracking
        main_cell = random.choice(random.choice(grid))
        backtracking = []
        while True:
            if not main_cell.dead_end:
                backtracking.append(main_cell)
                main_cell = main_cell.wall_test_RB(grid)
            else:
                del backtracking[len(backtracking) - 1]
                if len(backtracking) == 0:
                    break
                main_cell = backtracking[len(backtracking) - 1]
    for line in grid:
        for item in line:
            maze_map[item.i*2+1][item.j*2+1] = LETTER_CORRIDOR
            if item.up == False:
                maze_map[item.i*2][item.j*2+1] = LETTER_CORRIDOR
            if item.down == False:
                maze_map[item.i*2+2][item.j*2+1] = LETTER_CORRIDOR
            if item.left == False:
                maze_map[item.i*2+1][item.j*2] = LETTER_CORRIDOR
            if item.right == False:
                maze_map[item.i*2+1][item.j*2+2] = LETTER_CORRIDOR
    make_room(maze_map)
    make_entrance_and_exit(maze_map, number_of_players)
    add_doors(maze_map)
    map_finished = make_str_from_2d_array(maze_map)
    return map_finished
