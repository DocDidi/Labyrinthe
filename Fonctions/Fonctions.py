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

# def save_game(game_screen):
#     """Sauvegarde la partie"""
#     with open(SAVE_FILE, "wb") as save_file:
#         save_file.write(pickle.dumps(game_screen))

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

# def finished_menu(maze, map_height, time_spent, steps, maze_menu_obj):
#     """Messages et menu de choix quand le labyrinthe est fini."""
#     map_already_saved = False
#     if maze_menu_obj.selected == 0:
#         map_already_saved = True
#     time_spent = str_time(time_spent)
#     print(WHITE_TEXT+MESSAGE_WIN.format(map_height +1,time_spent, steps))
#     no_input = True
#     while no_input:
#         x = keyboard_input(1)
#         if x == CTRL_C:
#             exit()
#         elif x.lower() == "q":
#             no_input = False
#             maze_menu_obj.chosen = False
#         elif ord(x) == 13 and not map_already_saved:
#             no_input = False
#         elif x.lower() == "s":
#             if map_already_saved:
#                 print(MESSAGE_MAP_ALREADY_SAVED.format(map_height+1))
#             else:
#                 save_maze(maze)
#                 no_input = False
#             maze_menu_obj.chosen = False

# def str_time(time_spent):
#     minutes = int(time_spent // 60)
#     seconds = int(time_spent % 60)
#     hours = minutes // 60
#     minutes == minutes % 60
#     if seconds <= 1:
#         word_seconds = WORD_SECOND
#     else:
#         word_seconds = WORD_SECONDS
#     if minutes <= 1:
#         word_minutes = WORD_MINUTE
#     else:
#         word_minutes = WORD_MINUTES
#     if not minutes and not hours:
#         return "{0} {1}".format(seconds,word_seconds)
#     elif not hours:
#         return "{0} {1}, {2} {3}"\
#         .format(minutes,word_minutes, seconds,word_seconds)
#     else:
#         return MESSAGE_HOUR_LONG

# def save_maze(maze):
#     """Sauvegarde le labyrinthe"""
#     go_for_save = False
#     while not go_for_save:
#         clear_and_display()
#         maze_file = input(maze+MESSAGE_SAVE_MAZE)
#         maze_file = MAPS_DIRECTORY + maze_file + MAPS_FORMAT
#         if os.path.exists(maze_file):
#             print(MESSAGE_SAVE_OVERWRITE)
#             choice = keyboard_input(1)
#             if choice == 'CTRL_C':
#                 exit()
#             if choice.lower() == ('o' or 'y'):
#                 go_for_save = True
#             if choice.lower() == 'q':
#                 break
#         else:
#             go_for_save = True
#     if go_for_save:
#         with open(maze_file, "w") as save_file:
#             save_file.write(maze)

# def print_path_taken(props, players):
#     """Affiche le chemin parcouru par les joueurs"""
#     for item in props:
#         if (type(item) == Corridor) and item.visited:
#             print("{0}\033[{1};{2}H{3}".format\
#             (B_BLUE_TEXT,item.y+1,item.x+1,\
#             SYMBOL_CORRIDOR_VISITED))
#     for player in players:
#         print(player)
