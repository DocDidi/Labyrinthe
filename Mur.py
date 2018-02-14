#! /usr/bin/env python3
# coding: utf-8

from var import *

class Mur:
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.revealed = False

    def __str__(self):
        return ("{0}\033[{1};{2}H{3}".format\
        (YELLOW_TEXT,self.y+1,self.x+1,SYMBOLEMUR))
