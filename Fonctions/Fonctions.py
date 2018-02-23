#! /usr/bin/env python3
# coding: utf-8

import os, pickle, sys, termios, tty
from Fonctions.Variables import *
from Fonctions.Variables_Map_Building import *
from Fonctions.Player import *
from Fonctions.Wall import *
from Fonctions.Door import *
from Fonctions.Corridor import *
from Fonctions.GenerateMaze import *
from Fonctions.StartMenu import *

def clear_and_display(*str_value):
    """Efface l'écran et positionne le curseur en haut a gauche.
    Peut prendre en entrée une chaine de caracteres à afficher"""
    print(CLEAR_SCREEN)
    if str_value == ():
        print(CURSOR_RESET)
    else:
        print(CURSOR_RESET + WHITE_TEXT + str(str_value[0]))

def check_screen_size(map_height, map_width):
    """Demande à l'utilisateur d'agrandir sa console si besoin."""
    CORRECT_HEIGHT = True
    CORRECT_WIDTH = True
    rows, columns = os.popen('stty size', 'r').read().split()
    while int(rows) < map_height + 3:
        CORRECT_HEIGHT = False
        rows, columns = os.popen('stty size', 'r').read().split()
        clear_and_display(MESSAGE_ERROR_SCREEN_HEIGHT)
    if CORRECT_HEIGHT == False:
        clear_and_display(MESSAGE_SCREEN_CORRECT)
        input()
    while int(columns) < map_width:
        CORRECT_WIDTH = False
        rows, columns = os.popen('stty size', 'r').read().split()
        clear_and_display(MESSAGE_ERROR_SCREEN_WIDTH)
    if CORRECT_WIDTH == False:
        clear_and_display(MESSAGE_SCREEN_CORRECT)
        input()

def maze_display(players, props, map_height, map_width):
    """Affiche le labyrinthe."""
    maze_map = ""
    for item in props:
        maze_map = maze_map + str(item)
    clear_and_display(maze_map)
    for player in players:
        print(player)
    if len(players)>1:
        print(MESSAGE_MOVES_MULTI.format(map_height + 2))
    else:
        print(WHITE_TEXT + MESSAGE_MOVES.format(map_height + 2))

def save_game(players, props, map_height, map_width, maze):
    """Sauvegarde la partie"""
    with open(SAVE_FILE, "wb") as save_file:
        save_file.write\
        (pickle.dumps((players, props, map_height, map_width, maze)))

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

def extract_data_from_map(maze_map):
    """Extrait les données du jeu de la carte (str)
    Renvoie players, props, map_height, map_width"""
    lines = maze_map.split("\n")
    join_with = (LETTER_WALL, LETTER_DOOR, LETTER_END)
    props = []
    players = []
    check_player = False
    check_end = False
    check_key = False
    for i, line in enumerate(lines):
        for j, letter in enumerate(line):
            if letter is LETTER_PLAYER[0]:
                players.append(Player(i,j))
                props.append(Corridor(i,j))
                check_player = True
            if letter is LETTER_PLAYER[1]:
                players.append(Player(i,j,player_number = 2))
                props.append(Corridor(i,j))
            elif letter is LETTER_END:
                vertical = False
                if j == 0 or j == len(line)-1:
                    vertical = True
                props.append(Door(i,j,vertical,end = True))
                check_end = True
            elif letter is LETTER_DOOR:
                vertical = False
                if lines[i][j+1] == LETTER_CORRIDOR\
                or lines[i][j-1] == LETTER_CORRIDOR:
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
                check_key = True
            else:
                props.append(Corridor(i,j))
    if check_player and check_end and check_key:
        return(players, props, i, j)
    else:
        return extract_data_from_map(DEFAULT_MAP)

def player_move(players, props, LabyOn, map_height, maze_menu_obj):
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
            LabyOn = False
            maze_menu_obj.chosen = False
        elif x.lower()=='d':
            cheatcode = 1
        elif x.lower()=='o' and cheatcode == 1:
            cheatcode = 2
        elif x.lower()=='c' and cheatcode == 2:
            for item in props:
                item.revealed = True
            no_input = False
        elif x.lower()=='g':
            for item in props:
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

    for player in players:
        player.move(player_to_move, movement,props)

    return (LabyOn)

def keyboard_input(nbl):
    """Renvoie la ou les touches de clavier pressées.
    Prend le nombre de touches à renvoyer"""
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin)
    text_grab=sys.stdin.read(nbl)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
    return text_grab

def check_if_lit(item, players):
    """Calcule si l'objet est éclairé"""
    item.lit = False
    for player in players:
        if ((-2 <= player.x - item.x <= 2) and (-3 <= player.y - item.y <= 3))\
        or ((-3 <= player.x - item.x <= 3) and (-2 <= player.y - item.y <= 2)):
            item.revealed = True
        if ((-1 <= player.x - item.x <= 1) and (-2 <= player.y - item.y <= 2))\
        or ((-2 <= player.x - item.x <= 2) and (-1 <= player.y - item.y <= 1)):
            item.lit = True
        if player.x == item.x and player.y == item.y:
            item.visited = True

def check_fog(players, props):
    """Liste les choses à reveler et les passe a la fonction check_if_lit"""
    for item in props:
        check_if_lit(item, players)

def finished_menu(maze, map_height, time_spent, steps, maze_menu_obj):
    """Messages et menu de choix quand le labyrinthe est fini."""
    map_already_saved = False
    if maze_menu_obj.selected == 0:
        map_already_saved = True
    time_spent = str_time(time_spent)
    print(WHITE_TEXT+MESSAGE_WIN.format(map_height +1,time_spent, steps))
    no_input = True
    while no_input:
        x = keyboard_input(1)
        if x == CTRL_C:
            exit()
        elif x.lower() == "q":
            no_input = False
            maze_menu_obj.chosen = False
        elif ord(x) == 13:
            no_input = False
        elif x.lower() == "s":
            if map_already_saved:
                print(MESSAGE_MAP_ALREADY_SAVED.format(map_height+1))
            else:
                save_maze(maze)
                no_input = False
            maze_menu_obj.chosen = False

def str_time(time_spent):
    minutes = int(time_spent // 60)
    seconds = int(time_spent % 60)
    hours = minutes // 60
    minutes == minutes % 60
    if seconds <= 1:
        word_seconds = WORD_SECOND
    else:
        word_seconds = WORD_SECONDS
    if minutes <= 1:
        word_minutes = WORD_MINUTE
    else:
        word_minutes = WORD_MINUTES
    if not minutes and not hours:
        return "{0} {1}".format(seconds,word_seconds)
    elif not hours:
        return "{0} {1}, {2} {3}"\
        .format(minutes,word_minutes, seconds,word_seconds)
    else:
        return MESSAGE_HOUR_LONG

def save_maze(maze):
    """Sauvegarde le labyrinthe"""
    go_for_save = False
    while not go_for_save:
        clear_and_display()
        maze_file = input(maze+MESSAGE_SAVE_MAZE)
        maze_file = MAPS_DIRECTORY + maze_file + MAPS_FORMAT
        if os.path.exists(maze_file):
            print(MESSAGE_SAVE_OVERWRITE)
            choice = keyboard_input(1)
            if choice == 'CTRL_C':
                exit()
            if choice.lower() == ('o' or 'y'):
                go_for_save = True
            if choice.lower() == 'q':
                break
        else:
            go_for_save = True
    if go_for_save:
        with open(maze_file, "w") as save_file:
            save_file.write(maze)

def print_path_taken(props, players):
    """Affiche le chemin parcouru par les joueurs"""
    for item in props:
        if (type(item) == Corridor) and item.visited:
            print("{0}\033[{1};{2}H{3}".format\
            (B_BLUE_TEXT,item.y+1,item.x+1,\
            SYMBOL_CORRIDOR_VISITED))
    for player in players:
        print(player)
