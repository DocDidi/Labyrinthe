#! /usr/bin/env python3
# coding: utf-8

import os, pickle, sys, termios, tty, os
from Fonctions.Variables import *

def load_file():
    """Propose de reprendre la partie précedente"""
    if os.path.exists(SAVE_FILE):
        print(WHITE_TEXT + MESSAGE_LOAD_MAZE)
        choice = keyboard_input(1)
        if choice == CTRL_C:
            os.system('clear')
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

def keyboard_input(nbl):
    """Renvoie la ou les touches de clavier pressées.
    Prend le nombre de touches à renvoyer"""
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin)
    text_grab=sys.stdin.read(nbl)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
    return text_grab
