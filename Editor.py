#! /usr/bin/env python3
# coding: utf-8

from Fonctions.Variables import *
from Fonctions.StartMenu import *
from Fonctions.GameScreen import *
from Fonctions.Player import *
from Fonctions.Wall import *
from Fonctions.Door import *
from Fonctions.Corridor import *



class Editor():
    def __init__(self):
        self.selected = 0
        self.chosen = False
        self.file_index = 0
        self.choice = []
        self.file_path = MAPS_LOAD.find("*")
        self.maze = ""
        self.x = 0
        self.y = 0

    def __str__(self):
        self.directory_content = glob.glob(MAPS_LOAD)
        self.min_choice = 0
        if not self.directory_content:
            self.saved_maps = (MESSAGE_ERROR_DIRECTORY.format(MAPS_DIRECTORY))
            self.selected = 1
            self.min_choice = 1
        else:
            self.saved_maps = MESSAGE_MAP_LOAD+self.directory_content\
            [self.file_index][self.file_path:-4].capitalize()
        self.choice = [self.saved_maps] + [MESSAGE_MAP_CHOICE_QUIT]
        result_str = ""
        for i, maze_map in enumerate(self.choice):
            if i == self.selected:
                result_str += \
                BLACK_ON_WHITE + maze_map + WHITE_TEXT
            else:
                if maze_map == MESSAGE_MAP_CHOICE_QUIT:
                    result_str += B_RED_TEXT + maze_map
                else:
                    result_str += WHITE_TEXT + maze_map
            result_str += "\n"
        return result_str


    def maze_menu(self):
        """Menu de selection des cartes.
        Renvoie le nom du maze_file choisi ou la carte aléatoire."""
        while not self.chosen:
            no_input = True
            while no_input:
                print(CLEAR_SCREEN + CURSOR_RESET)
                print(self)
                choice = self.keyboard_input(1)
                if choice == CTRL_C:
                    os.system('clear')
                    exit()
                elif ord(choice) == 13:
                    self.chosen = \
                    self.choice[self.selected]
                    no_input = False
                elif choice == ESCAPE_CHARACTER:
                    addendum = self.keyboard_input(2)
                    choice = choice + addendum
                elif ord(choice) == 127:
                    os.system('clear')
                    exit()
                if choice==ARROW_DOWN:
                    if self.selected < (len(self.choice)-1):
                        self.selected += 1
                    no_input = False
                elif choice==ARROW_UP:
                    if self.selected > self.min_choice:
                        self.selected -= 1
                    no_input = False
                elif choice==ARROW_LEFT and self.file_index > 0:
                    self.file_index -= 1
                    no_input = False
                elif choice==ARROW_RIGHT \
                and self.file_index<len(self.directory_content)-1:
                    self.file_index += 1
                    no_input = False
        if self.chosen == self.saved_maps and self.directory_content:
            self.chosen = self.directory_content[self.file_index]
            if os.path.exists(self.chosen):
                with open(self.chosen, "r") as maze_map:
                    self.maze = maze_map.read()
        # elif self.chosen == MESSAGE_MAP_CHOICE_RANDOM_SMALL:
        #     maze_map = make_maze(SMALL_WIDTH,SMALL_HEIGHT)
        #     return maze_map
        # elif self.chosen == MESSAGE_MAP_CHOICE_RANDOM_BIG:
        #     maze_map = make_maze(BIG_WIDTH,BIG_HEIGHT)
        #     return maze_map
        # elif self.chosen == MESSAGE_MAP_CHOICE_RANDOM_SCREEN:
        #     rows, columns = os.popen('stty size', 'r').read().split()
        #     maze_map = make_maze(int(columns)-1,int(rows)-4)
        #     return maze_map
        # elif self.chosen == MESSAGE_MAP_CHOICE_RANDOM_BIG_MULTIPLAYER:
        #     maze_map = make_maze(BIG_WIDTH,BIG_HEIGHT, number_of_players=2)
        #     return maze_map
        # elif self.chosen == MESSAGE_MAP_CHOICE_RANDOM_SCREEN_MULTIPLAYER:
        #     rows, columns = os.popen('stty size', 'r').read().split()
        #     maze_map = make_maze(int(columns)-1,int(rows)-4,number_of_players=2)
        #     return maze_map
        elif self.chosen == MESSAGE_MAP_CHOICE_QUIT:
            os.system('clear')
            exit()

    def display(self):
        lines = self.maze.split("\n")
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
                    if j == 0 or j == len(line)-1:
                        vertical = True
                    props.append(Door(i,j,vertical,end = True))
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
                else:
                    props.append(Corridor(i,j))
        self.players = players
        self.props = props
        self.height = i
        self.width = j
        maze_map = ""
        for item in self.props:
            item.revealed = True
            maze_map += str(item)
            if item.x == self.width:
                maze_map += "\n"
        print(CLEAR_SCREEN + CURSOR_RESET + maze_map)
        for player in self.players:
            player.display(0,1)
        print(WHITE_TEXT + "\033[{0};{1}f█".format(self.y+1, self.x+1))
        print("\033[{0}H{1},{2}".format(self.height + 1,self.x,self.y))



    def edit(self):
        no_input = True
        while no_input:
            choice = self.keyboard_input(1)
            if choice == CTRL_C:
                os.system('clear')
                exit()
            elif choice == ESCAPE_CHARACTER:
                addendum = self.keyboard_input(2)
                choice = choice + addendum
            elif choice.lower()=="k":
                no_input = False
                maze_map=[]
                lines = self.maze.split("\n")
                for i, line in enumerate(lines):
                    maze_map.append([])
                    for letter in line:
                        maze_map[i].append(letter)
                if maze_map[self.y][self.x] != LETTER_KEY:
                    maze_map[self.y][self.x] = LETTER_KEY
                elif maze_map[self.y][self.x] == LETTER_KEY:
                    maze_map[self.y][self.x] = LETTER_CORRIDOR
                groundwork_str=""
                for line in maze_map:
                    for letter in line:
                        groundwork_str += letter
                    groundwork_str += "\n"
                groundwork_str = groundwork_str[:-1]
                self.maze = groundwork_str
            elif choice.lower()=="d":
                no_input = False
                maze_map=[]
                lines = self.maze.split("\n")
                for i, line in enumerate(lines):
                    maze_map.append([])
                    for letter in line:
                        maze_map[i].append(letter)
                if maze_map[self.y][self.x] != LETTER_DOOR:
                    maze_map[self.y][self.x] = LETTER_DOOR
                elif maze_map[self.y][self.x] == LETTER_DOOR:
                    maze_map[self.y][self.x] = LETTER_CORRIDOR
                groundwork_str=""
                for line in maze_map:
                    for letter in line:
                        groundwork_str += letter
                    groundwork_str += "\n"
                groundwork_str = groundwork_str[:-1]
                self.maze = groundwork_str
            elif choice.lower()=="p":
                no_input = False
                maze_map=[]
                lines = self.maze.split("\n")
                for i, line in enumerate(lines):
                    maze_map.append([])
                    for letter in line:
                        maze_map[i].append(letter)
                if maze_map[self.y][self.x] != LETTER_PLAYER[0] \
                and maze_map[self.y][self.x] != LETTER_PLAYER[1]:
                    maze_map[self.y][self.x] = LETTER_PLAYER[0]
                elif maze_map[self.y][self.x] == LETTER_PLAYER[0]:
                    maze_map[self.y][self.x] = LETTER_PLAYER[1]
                elif maze_map[self.y][self.x] == LETTER_PLAYER[1]:
                    maze_map[self.y][self.x] = LETTER_CORRIDOR
                groundwork_str=""
                for line in maze_map:
                    for letter in line:
                        groundwork_str += letter
                    groundwork_str += "\n"
                groundwork_str = groundwork_str[:-1]
                self.maze = groundwork_str
            elif ord(choice) == 32:
                no_input = False
                maze_map=[]
                lines = self.maze.split("\n")
                for i, line in enumerate(lines):
                    maze_map.append([])
                    for letter in line:
                        maze_map[i].append(letter)
                if maze_map[self.y][self.x] != LETTER_CORRIDOR:
                    maze_map[self.y][self.x] = LETTER_CORRIDOR
                elif maze_map[self.y][self.x] == LETTER_CORRIDOR:
                    maze_map[self.y][self.x] = LETTER_WALL
                groundwork_str=""
                for line in maze_map:
                    for letter in line:
                        groundwork_str += letter
                    groundwork_str += "\n"
                groundwork_str = groundwork_str[:-1]
                self.maze = groundwork_str
            if choice==ARROW_DOWN and self.y < self.height - 1:
                self.y+=1
                no_input = False
            elif choice==ARROW_UP and self.y > 0:
                self.y-=1
                no_input = False
            elif choice==ARROW_LEFT and self.x > 0:
                self.x-=1
                no_input = False
            elif choice==ARROW_RIGHT and self.x < self.width:
                self.x+=1
                no_input = False



    def keyboard_input(self, nbl):
        """Renvoie la ou les touches de clavier pressées.
        Prend le nombre de touches à renvoyer"""
        orig_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        text_grab=sys.stdin.read(nbl)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
        return text_grab


editor = Editor()
editor.maze_menu()
while True:
    editor.display()
    editor.edit()
