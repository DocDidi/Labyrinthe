#! /usr/bin/env python3
# coding: utf-8


# KRUSKAL


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

    def wall_test(self, grid, indexed_list):
        """Pick a random direction and break the wall if possible"""
        tries = ["Up","Down","Left","Right"]
        random.shuffle(tries)
        for x in tries:
            if x == "Up" and self.i-1 > 0:
                target_cell = grid[self.i-1][self.j]
                if target_cell.index_value != self.index_value:
                    change_index\
                    (target_cell.index_value,self.index_value,indexed_list)
                    self.up = False
            if x == "Down" and self.i+1 < len(grid)-1:
                target_cell = grid[self.i+1][self.j]
                if target_cell.index_value != self.index_value:
                    change_index\
                    (target_cell.index_value,self.index_value,indexed_list)
                    self.down = False
            if x == "Left" and self.j-1 > 0:
                target_cell = grid[self.i][self.j-1]
                if target_cell.index_value != self.index_value:
                    change_index\
                    (target_cell.index_value,self.index_value,indexed_list)
                    self.left = False
            if x == "Right" and self.j+1 < len(grid[0])-1:
                    target_cell = grid[self.i][self.j+1]
                    if target_cell.index_value != self.index_value:
                        change_index\
                        (target_cell.index_value,self.index_value,indexed_list)
                        self.right = False

def change_index(a, b, indexed_list):
    """Modify the indexes after a wall broke"""
    value_low = min(a, b)
    value_high = max(a, b)
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
    number_of_rooms = (len(maze_map)*len(maze_map[1])) // 25
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
        cell_active.wall_test(grid, indexed_list)
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

if __name__ == '__main__':
    # maze_map = make_maze(150,35,number_of_players = 2)
    # print(maze_map)
    import time

    w = 50
    h = 25

    SYMBOL_WALL = "\U00002338"
    SYMBOL_WALL_N = "\U0000257d"
    SYMBOL_WALL_S = "\U0000257f"
    SYMBOL_WALL_E = "\U0000257e"
    SYMBOL_WALL_W = "\U0000257c"
    SYMBOL_WALL_EW = "\U00002550"
    SYMBOL_WALL_NS = "\U00002551"
    SYMBOL_WALL_SE = "\U00002554"
    SYMBOL_WALL_SW = "\U00002557"
    SYMBOL_WALL_NE = "\U0000255A"
    SYMBOL_WALL_NW = "\U0000255D"
    SYMBOL_WALL_NSE = "\U00002560"
    SYMBOL_WALL_NSW = "\U00002563"
    SYMBOL_WALL_SEW = "\U00002566"
    SYMBOL_WALL_NEW = "\U00002569"
    SYMBOL_WALL_NSEW = "\U0000256C"
    SYMBOL_DOOR = "\U0000254D"
    SYMBOL_DOOR_VERTICAL = "\U0000254F"
    SYMBOL_PLAYER = "\U0000229a"
    SYMBOL_CORRIDOR = " "
    SYMBOL_CORRIDOR_VISITED = "\U000022C5"
    SYMBOL_FOG = "\U00002425"
    SYMBOL_KEY = "\U000026b7"
    BLACK_ON_WHITE = "\033[0;1;30;47m"
    RED_TEXT = "\033[31m"
    GREEN_TEXT = "\033[32m"
    YELLOW_TEXT = "\033[33m"
    BLUE_TEXT = "\033[34m"
    MAGENTA_TEXT = "\033[35m"
    CYAN_TEXT = "\033[36m"
    WHITE_TEXT = "\033[37m"
    B_RED_TEXT = "\033[1;31m"
    B_GREEN_TEXT = "\033[1;32m"
    B_YELLOW_TEXT = "\033[1;33m"
    B_BLUE_TEXT = "\033[1;34m"
    B_MAGENTA_TEXT = "\033[1;35m"
    B_CYAN_TEXT = "\033[1;36m"
    B_WHITE_TEXT = "\033[1;37m"
    CLEAR_SCREEN = '\033[2J'
    CURSOR_RESET = '\033[H'
    CLR_ATTR = "\033[0m"

    COLOR_PLAYER_1 = B_BLUE_TEXT
    COLOR_PLAYER_2 = B_RED_TEXT

    class Wall:
        def __init__(self, y, x, neighbors = False):
            self.x = x
            self.y = y
            self.end = False
            self.neighbors = neighbors
            self.has_key = False

            if self.neighbors == "N":
                self.symbol = SYMBOL_WALL_N
            elif self.neighbors == "S":
                self.symbol = SYMBOL_WALL_S
            elif self.neighbors == "E":
                self.symbol = SYMBOL_WALL_E
            elif self.neighbors == "W":
                self.symbol = SYMBOL_WALL_W
            elif self.neighbors == "EW":
                self.symbol = SYMBOL_WALL_EW
            elif self.neighbors == "NS":
                self.symbol = SYMBOL_WALL_NS
            elif self.neighbors == "SE":
                self.symbol = SYMBOL_WALL_SE
            elif self.neighbors == "SW":
                self.symbol = SYMBOL_WALL_SW
            elif self.neighbors == "NE":
                self.symbol = SYMBOL_WALL_NE
            elif self.neighbors == "NW":
                self.symbol = SYMBOL_WALL_NW
            elif self.neighbors == "NSE":
                self.symbol = SYMBOL_WALL_NSE
            elif self.neighbors == "NSW":
                self.symbol = SYMBOL_WALL_NSW
            elif self.neighbors == "SEW":
                self.symbol = SYMBOL_WALL_SEW
            elif self.neighbors == "NEW":
                self.symbol = SYMBOL_WALL_NEW
            elif self.neighbors == "NSEW":
                self.symbol = SYMBOL_WALL_NSEW
            else:
                self.symbol = SYMBOL_WALL

        def __str__(self):
            return YELLOW_TEXT+self.symbol+CLR_ATTR


    class Corridor:
        def __init__(self, y, x, has_key = False):
            self.x = x
            self.y = y
            self.end = False
            self.has_key = has_key

        def __str__(self):
            symbol = SYMBOL_CORRIDOR
            if self.has_key:
                symbol = SYMBOL_KEY

            return WHITE_TEXT+symbol+CLR_ATTR

    class Door:
        def __init__(self, y, x, vertical, end = False):
            self.x = x
            self.y = y
            self.end = end
            self.vertical = vertical
            self.has_key = False

        def __str__(self):
            if self.end == True:
                color = RED_TEXT
            else:
                color = YELLOW_TEXT
            if self.vertical == True :
                symbol = SYMBOL_DOOR_VERTICAL
            else :
                symbol = SYMBOL_DOOR

            return color+symbol+CLR_ATTR

    class Player:
        def __init__(self, y, x, player_number = 1):
            self.x = x
            self.y = y
            self.player_number = player_number



    def display(maze_map):
        lines = maze_map.split("\n")
        join_with = (LETTER_WALL, LETTER_DOOR, LETTER_END)
        props = []
        players = []
        for i, line in enumerate(lines):
            for j, letter in enumerate(line):
                if letter is LETTER_PLAYER[0]:
                    players.append(Player(i,j))
                    props.append(Corridor(i,j))
                elif letter is LETTER_PLAYER[1]:
                    players.append(Player(i,j,player_number = 2))
                    props.append(Corridor(i,j))
                elif letter is LETTER_END:
                    vertical = False
                    if j < len(line)-1:
                        if lines[i][j+1] not in join_with:
                            vertical = True
                    if j > 0:
                        if lines[i][j-1] not in join_with:
                            vertical = True
                    props.append(Door(i,j,vertical,end = True))
                elif letter is LETTER_DOOR:
                    vertical = False
                    if j < len(line)-1:
                        if lines[i][j+1] not in join_with:
                            vertical = True
                    if j > 0:
                        if lines[i][j-1] not in join_with:
                            vertical = True
                    props.append(Door(i,j,vertical))
                elif letter is LETTER_WALL:
                    neighbors = ""
                    if i>0:
                        if lines[i-1][j] in join_with:
                            neighbors += "N"
                    if i<(len(lines)-2):
                        if lines[i+1][j] in join_with:
                            neighbors += "S"
                    if j<(len(lines[0])-1):
                        if lines[i][j+1] in join_with:
                            neighbors += "E"
                    if j>0:
                        if lines[i][j-1] in join_with:
                            neighbors += "W"
                    props.append(Wall(i,j,neighbors))
                elif letter is LETTER_KEY:
                    props.append(Corridor(i,j,has_key=True))
                else:
                    props.append(Corridor(i,j))
        maze_display = ""
        for item in props:
            is_not_player = True
            item.revealed = True
            for player in players:
                if (item.x,item.y) == (player.x,player.y):
                    is_not_player = False
                    if player.player_number == 1:
                        color = B_BLUE_TEXT
                    else:
                        color = B_RED_TEXT
                    maze_display += color + SYMBOL_PLAYER + CLR_ATTR
            if is_not_player:
                maze_display += item.__str__()
            if item.x == w:
                maze_display += "\n"
        print(CLEAR_SCREEN + CURSOR_RESET + maze_display)



    number_of_players = 1
    grid = make_grid(w,h)
    maze_map = groundwork(w,h)
    list_of_cells = []
    for line in grid:
        for item in line:
            list_of_cells.append(item)
    indexed_list = []
    for item in list_of_cells:
        new_list = [item]
        indexed_list.append(new_list)
    random.shuffle(list_of_cells)
    map_finished = make_str_from_2d_array(maze_map)
    display(map_finished)
    i = 1
    for cell_active in list_of_cells:
        map_test = make_str_from_2d_array(maze_map)
        cell_active.wall_test(grid, indexed_list)
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
        map_finished = make_str_from_2d_array(maze_map)
        if map_finished !=  map_test:
            time.sleep(0.1)
            display(map_finished)
        i+=1
    time.sleep(0.5)
    number_of_rooms = (len(maze_map)*len(maze_map[1])) // 25
    key_placed = False
    eligible_spots = []
    if len(maze_map) > 3 and len(maze_map[0]) > 3:
        for i in range(2, len(maze_map) -1, 2):
            for j in range(2, len(maze_map[0]) -1, 2):
                eligible_spots.append((i,j))
        random.shuffle(eligible_spots)
        i = 1
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
            map_finished = make_str_from_2d_array(maze_map)
            display(map_finished)
            i+=1
            time.sleep(0.1)
    make_entrance_and_exit(maze_map, number_of_players)
    map_finished = make_str_from_2d_array(maze_map)
    display(map_finished)
    time.sleep(0.5)
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
                    map_finished = make_str_from_2d_array(maze_map)
                    display(map_finished)
                    time.sleep(0.1)
