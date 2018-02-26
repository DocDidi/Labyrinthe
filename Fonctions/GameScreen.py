#! /usr/bin/env python3
# coding: utf-8

import os, time, pickle, termios, tty, sys
from Fonctions.Variables import *
from Fonctions.Variables_Map_Building import *
# from Fonctions.Fonctions import *
from Fonctions.Player import *
from Fonctions.Wall import *
from Fonctions.Door import *
from Fonctions.Corridor import *


class GameScreen:

    def __init__(self, maze, start_menu):
        """Extrait les données du jeu de la carte (str)"""
        lines = maze.split("\n")
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
                elif letter is LETTER_PLAYER[1]:
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
            self.players = players
            self.props = props
            self.height = i
            self.width = j
            self.maze = maze
        else:
            self.__init__(DEFAULT_MAP)

        self.start_menu = start_menu
        self.player_have_key = False
        self.maze_on = True
        self.time_start = 0
        self.time_spent = ""

    def start(self):
        self.maze_on = True
        self.player_have_key = False
        self.start_timer()

    def save_game(self):
        """Sauvegarde la partie"""
        with open(SAVE_FILE, "wb") as save_file:
            save_file.write(pickle.dumps(self))

    def display(self):
        self.check_screen_size()
        for item in self.props:
            item.lit = False
            for player in self.players:
                if ((-2 <= player.x - item.x <= 2) \
                and (-3 <= player.y - item.y <= 3))\
                or ((-3 <= player.x - item.x <= 3) \
                and (-2 <= player.y - item.y <= 2)):
                    item.revealed = True
                if ((-1 <= player.x - item.x <= 1) \
                and (-2 <= player.y - item.y <= 2))\
                or ((-2 <= player.x - item.x <= 2) \
                and (-1 <= player.y - item.y <= 1)):
                    item.lit = True
                if player.x == item.x and player.y == item.y:
                    item.visited = True
        maze_map = CLEAR_SCREEN + CURSOR_RESET
        for item in self.props:
            maze_map += str(item)
            if item.x == self.width:
                maze_map += "\n"
        print(maze_map)
        for player in self.players:
            print(player)
        if self.player_have_key:
            print(WHITE_TEXT + "\033[{0}H{1}\033[1B"\
            .format(self.height + 1, SYMBOL_KEY))
        else:
            print(WHITE_TEXT + "\033[{0}H{1}\033[1B"\
            .format(self.height + 1, MESSAGE_KEY))
        if len(self.players)>1:
            print(MESSAGE_MOVES_MULTI.format(self.height + 2))
        else:
            print(WHITE_TEXT + MESSAGE_MOVES.format(self.height + 2))
        self.save_game()

    def player_move(self):
        """Capture les touches pour faire bouger le joueur"""
        no_input = True
        player_to_move = 0
        movement = ""
        cheatcode = 0
        while no_input:
            choice = self.keyboard_input(1)
            if choice == CTRL_C:
                exit()
            elif ord(choice) == 127:
                no_input = False
                self.maze_on = False
                self.start_menu.chosen = False
            elif choice.lower()=='p':
                cheatcode = 1
            elif choice.lower()=='o' and cheatcode == 1:
                cheatcode = 2
            elif choice.lower()=='u' and cheatcode == 2:
                cheatcode = 3
            elif choice.lower()=='e' and cheatcode == 3:
                cheatcode = 4
            elif choice.lower()=='t' and cheatcode == 4:
                for item in self.props:
                    item.revealed = True
                no_input = False
            elif choice.lower()=='g':
                for item in self.props:
                    try:
                        item.neighbors = False
                    except:
                        pass
                no_input = False
            elif choice.lower()=='z':
                player_to_move = 2
                movement = "U"
                no_input = False
            elif choice.lower()=='s':
                player_to_move = 2
                movement = "D"
                no_input = False
            elif choice.lower()=='d':
                player_to_move = 2
                movement = "R"
                no_input = False
            elif choice.lower()=='q':
                player_to_move = 2
                movement = "L"
                no_input = False
            elif choice == ESCAPE_CHARACTER:
                addendum = self.keyboard_input(2)
                choice = choice + addendum
            if choice==ARROW_UP:
                player_to_move = 1
                movement = "U"
                no_input = False
            elif choice==ARROW_DOWN:
                player_to_move = 1
                movement = "D"
                no_input = False
            elif choice==ARROW_RIGHT:
                player_to_move = 1
                movement = "R"
                no_input = False
            elif choice==ARROW_LEFT:
                player_to_move = 1
                movement = "L"
                no_input = False

        for player in self.players:
            player.move(player_to_move, movement,self.props)

    def tests(self):
        """Déverouille la porte si la clé a été ramassée
        et vérifie que le jeu n'est pas encore fini."""
        for item in self.props:
            if self.player_have_key and item.end:
                item.block = False
            if item.has_key:
                for player in self.players:
                    if (player.x, player.y) == (item.x, item.y):
                        item.has_key = False
                        self.player_have_key = True
            if item.end:
                for player in self.players:
                    if (player.x, player.y) == (item.x, item.y):
                        self.maze_on = False
                        self.finished_menu()


    def check_screen_size(self):
        """Demande à l'utilisateur d'agrandir sa console si besoin."""
        CORRECT_HEIGHT = True
        CORRECT_WIDTH = True
        rows, columns = os.popen('stty size', 'r').read().split()
        while int(rows) < self.height + 3:
            CORRECT_HEIGHT = False
            rows, columns = os.popen('stty size', 'r').read().split()
            print(CLEAR_SCREEN + MESSAGE_ERROR_SCREEN_HEIGHT)
        if CORRECT_HEIGHT == False:
            print(CLEAR_SCREEN + MESSAGE_SCREEN_CORRECT)
            input()
        while int(columns) < self.width:
            CORRECT_WIDTH = False
            rows, columns = os.popen('stty size', 'r').read().split()
            print(CLEAR_SCREEN + MESSAGE_ERROR_SCREEN_WIDTH)
        if CORRECT_WIDTH == False:
            print(CLEAR_SCREEN + MESSAGE_SCREEN_CORRECT)
            input()

    def start_timer(self):
        """Démarre le chrono"""
        self.time_start = time.time()

    def stop_timer(self):
        """Arrete le chrono"""
        total_time = time.time() - self.time_start
        minutes = int(total_time // 60)
        seconds = int(total_time % 60)
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
            self.time_spent = "{0} {1}".format(seconds,word_seconds)
        elif not hours:
            self.time_spent =  "{0} {1}, {2} {3}"\
            .format(minutes,word_minutes, seconds,word_seconds)
        else:
            self.time_spent =  MESSAGE_HOUR_LONG

    def save_maze(self):
        """Sauvegarde le labyrinthe"""
        go_for_save = False
        while not go_for_save:
            print(CLEAR_SCREEN + CURSOR_RESET)
            maze_file = input(self.maze+MESSAGE_SAVE_MAZE)
            maze_file = MAPS_DIRECTORY + maze_file + MAPS_FORMAT
            if os.path.exists(maze_file):
                print(MESSAGE_SAVE_OVERWRITE)
                choice = self.keyboard_input(1)
                if choice == 'CTRL_C':
                    exit()
                if choice.lower() == ('o' or 'y'):
                    go_for_save = True
                if ord(choice) == 127:
                    break
            else:
                go_for_save = True
        if go_for_save:
            with open(maze_file, "w") as save_file:
                save_file.write(self.maze)

    def print_path_taken(self):
        """Affiche le chemin parcouru par les joueurs"""
        for item in self.props:
            if (type(item) == Corridor) and item.visited:
                print("{0}\033[{1};{2}H{3}".format\
                (B_BLUE_TEXT,item.y+1,item.x+1,\
                SYMBOL_CORRIDOR_VISITED))
        for player in self.players:
            print(player)

    def keyboard_input(self, nbl):
        """Renvoie la ou les touches de clavier pressées.
        Prend le nombre de touches à renvoyer"""
        orig_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        text_grab=sys.stdin.read(nbl)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
        return text_grab

    def finished_menu(self):
        """Messages et menu de choix quand le labyrinthe est fini."""
        for item in self.props:
            item.revealed = True
        self.display()
        os.remove(SAVE_FILE)
        self.stop_timer()
        self.print_path_taken()
        steps = 0
        for player in self.players:
            steps += player.step
        map_already_saved = False
        if self.start_menu.selected == 0:
            map_already_saved = True
        print(WHITE_TEXT + \
        MESSAGE_WIN.format(self.height +1,self.time_spent, steps))
        no_input = True
        while no_input:
            choice = self.keyboard_input(1)
            if choice == CTRL_C:
                exit()
            elif ord(choice) == 127:
                no_input = False
                self.start_menu.chosen = False
            elif ord(choice) == 13 and not map_already_saved:
                no_input = False
            elif choice.lower() == "s":
                if map_already_saved:
                    print(MESSAGE_MAP_ALREADY_SAVED.format(self.height+1))
                else:
                    self.save_maze()
                    no_input = False
                self.start_menu.chosen = False
