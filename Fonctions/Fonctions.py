#! /usr/bin/env python3
# coding: utf-8

import os, pickle, sys, termios, tty
from Fonctions.Variables import *
from Fonctions.GenerateMaze import *
from Fonctions.StartMenu import *
from Fonctions.GameScreen import *

def clear_and_display(*str_value):
    """Efface l'écran et positionne le curseur en haut a gauche.
    Peut prendre en entrée une chaine de caracteres à afficher"""
    print(CLEAR_SCREEN)
    if str_value == ():
        print(CURSOR_RESET)
    else:
        print(CURSOR_RESET + WHITE_TEXT + str(str_value[0]))

def load_file():
    """Propose de reprendre la partie précedente
    Renvoie un Tuple contenant les players, props, map_height, map_width
    qui étaient dans le maze_file"""
    if os.path.exists(SAVE_FILE):
        print(WHITE_TEXT + MESSAGE_LOAD_MAZE)
        choice = keyboard_input(1)
        if choice == 'CTRL_C':
            exit()
        elif choice.lower() == ('o' or 'y'):
            with open(SAVE_FILE, "rb") as save_file:
                ongoing_game = pickle.loads(save_file.read())
        else:
            os.remove(SAVE_FILE)
            ongoing_game = False
    else:
        ongoing_game = False
    return (ongoing_game)

def maze_menu(maze_menu_obj):
    """Menu de selection des cartes.
    Renvoie le nom du maze_file choisi ou la carte aléatoire."""
    while not maze_menu_obj.chosen:
        clear_and_display(B_BLUE_TEXT + MESSAGE_MAP_CHOICE)
        print(maze_menu_obj)
        no_input = True
        while no_input:
            x=keyboard_input(1)
            if x == CTRL_C:
                exit()
            elif ord(x) == 13:
                maze_menu_obj.chosen = \
                maze_menu_obj.choice[maze_menu_obj.selected]
                no_input = False
            elif x == ESCAPE_CHARACTER:
                y = keyboard_input(2)
                x = x+y
            elif x.lower()=='q':
                exit()
            if x==ARROW_DOWN:
                if maze_menu_obj.selected < (len(maze_menu_obj.choice)-1):
                    maze_menu_obj.selected += 1
                no_input = False
            elif x==ARROW_UP:
                if maze_menu_obj.selected > maze_menu_obj.min_choice:
                    maze_menu_obj.selected -= 1
                no_input = False
            elif x==ARROW_LEFT and maze_menu_obj.file_index > 0:
                maze_menu_obj.file_index -= 1
                no_input = False
            elif x==ARROW_RIGHT \
            and maze_menu_obj.file_index<len(maze_menu_obj.directory_content)-1:
                maze_menu_obj.file_index += 1
                no_input = False
    return maze_menu_obj.getmap()

def player_move(game_screen, maze_menu_obj):
    """Fait bouger le joueur
    Renvoie LabyOn == True si le jeu continue."""
    no_input = True
    player_to_move = 0
    movement = ""
    cheatcode = 0
    while no_input:
        x=keyboard_input(1)
        if x == CTRL_C:
            exit()
        elif x.lower()=='q':
            no_input = False
            game_screen.maze_on = False
            maze_menu_obj.chosen = False
        elif x.lower()=='d':
            cheatcode = 1
        elif x.lower()=='o' and cheatcode == 1:
            cheatcode = 2
        elif x.lower()=='c' and cheatcode == 2:
            for item in game_screen.props:
                item.revealed = True
            no_input = False
        elif x.lower()=='g':
            for item in game_screen.props:
                try:
                    item.neighbors = False
                except:
                    pass
            no_input = False
        elif x.lower()=='i':
            player_to_move = 2
            movement = "U"
            no_input = False
        elif x.lower()=='k':
            player_to_move = 2
            movement = "D"
            no_input = False
        elif x.lower()=='l':
            player_to_move = 2
            movement = "R"
            no_input = False
        elif x.lower()=='j':
            player_to_move = 2
            movement = "L"
            no_input = False
        elif x == ESCAPE_CHARACTER:
            y = keyboard_input(2)
            x = x+y
        if x==ARROW_UP:
            player_to_move = 1
            movement = "U"
            no_input = False
        elif x==ARROW_DOWN:
            player_to_move = 1
            movement = "D"
            no_input = False
        elif x==ARROW_RIGHT:
            player_to_move = 1
            movement = "R"
            no_input = False
        elif x==ARROW_LEFT:
            player_to_move = 1
            movement = "L"
            no_input = False

    for player in game_screen.players:
        player.move(player_to_move, movement,game_screen.props)

def keyboard_input(nbl):
    """Renvoie la ou les touches de clavier pressées.
    Prend le nombre de touches à renvoyer"""
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin)
    text_grab=sys.stdin.read(nbl)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
    return text_grab
