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
maze_menu_obj = StartMenu()

while GameOn:
    if ongoing_game:
        players, props, map_height, map_width, maze = ongoing_game
        ongoing_game = False
    else:
        maze = maze_menu(maze_menu_obj)
        players, props, map_height, map_width = extract_data_from_map(maze)
    check_screen_size(map_height, map_width)
    clear_and_display()
    LabyOn = True
    player_have_key = False
    start_time = time.time()
    while LabyOn:
        check_fog(players, props)
        maze_display(players, props, map_height, map_width)
        if player_have_key:
            print("\033[{0}H{1}\033[1B".format(map_height + 1, SYMBOL_KEY))
        else:
            print("\033[{0}H{1}\033[1B".format(map_height + 1, MESSAGE_KEY))
        LabyOn = player_move(players, props, LabyOn, map_height, maze_menu_obj)
        save_game(players, props, map_height, map_width, maze)
        for item in props:
            if player_have_key and item.end:
                item.block = False
            if item.has_key:
                for player in players:
                    if (player.x, player.y) == (item.x, item.y):
                        item.has_key = False
                        player_have_key = True
            if item.end:
                for player in players:
                    if (player.x, player.y) == (item.x, item.y):
                        LabyOn = False
                        os.remove(SAVE_FILE)
                        for item in props:
                            item.revealed = True
                        clear_and_display()
                        maze_display(players, props, map_height, map_width)
                        print_path_taken(props, players)
                        end_time = time.time()
                        time_spent = end_time - start_time
                        steps = 0
                        for player in players:
                            steps += player.step
                        finished_menu(maze, map_height, time_spent, steps,\
                        maze_menu_obj)
