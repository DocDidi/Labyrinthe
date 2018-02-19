#! /usr/bin/env python3
# coding: utf-8

import time

from Fonctions.Fonctions import *
from Fonctions.Variables import *

if OPERATING_SYSTEM == 'nt':
    print(MESSAGE_OS_INCOMPATIBILITY)
    exit()

GameOn = True
ongoing_game = load_file()
selected = 0

while GameOn:
    if ongoing_game:
        player, props, map_height, map_width, maze = ongoing_game
        ongoing_game = False
    else:
        maze, selected = maze_menu(selected)
        player, props, map_height, map_width = extract_data_from_map(maze)
    check_screen_size(map_height, map_width)
    clear_and_display()
    LabyOn = True
    start_time = time.time()
    while LabyOn:
        check_fog(player, props)
        maze_display(player, props, map_height, map_width)
        for item_end in props:
            if item_end.end:
                if (player.x, player.y) == (item_end.x, item_end.y):
                    LabyOn = False
                    os.remove(SAVE_FILE)
                    for item in props:
                        item.revealed = True
                    clear_and_display()
                    maze_display(player, props, map_height, map_width)
                    for item in props:
                        if (type(item) == Corridor) and item.visited:
                            print("{0}\033[{1};{2}H{3}".format\
                            (B_BLUE_TEXT,item.y+1,item.x+1,\
                            SYMBOL_CORRIDOR_VISITED))
                    end_time = time.time()
                    time_spent = end_time - start_time
                    finished_menu(maze, map_height, time_spent)
                    break
                else:
                    LabyOn = player_move(player, props, LabyOn, map_height)
                    save_game(player, props, map_height, map_width, maze)
