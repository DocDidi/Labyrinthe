#! /usr/bin/env python3
# coding: utf-8

from Fonctions.Variables import *

class Player:
    def __init__(self, y, x, player_number = 1):
        self.x = x
        self.y = y
        self.step = 0
        self.player_number = player_number

    def display(self, margin, margin_v):
        if self.player_number == 1:
            color = B_BLUE_TEXT
        else:
            color = B_RED_TEXT
        print("{0}\033[{1};{2}H{3}".format\
        (color,self.y+margin_v,self.x+1+margin,SYMBOL_PLAYER) + CLR_ATTR)

    def move(self,player_to_move, movement, props, width):
        """Move the player"""
        width = width + 1
        test_player_position = [self.y, self.x]
        if player_to_move == self.player_number:
            if movement == "U":
                test_player_position = [self.y - 1, self.x]
                test_item = props[(self.y - 1) * width + self.x]
            elif movement == "D":
                test_player_position = [self.y + 1, self.x]
                test_item = props[(self.y + 1) * width + self.x]
            elif movement == "R":
                test_player_position = [self.y ,self.x + 1]
                test_item = props[(self.y) * width + self.x + 1]
            elif movement == "L":
                test_player_position = [self.y, self.x - 1]
                test_item = props[(self.y) * width + self.x - 1]

            block = False
            if test_item.block == True:
                block = True
            if block == False:
                if (test_player_position[1] != self.x)\
                or (test_player_position[0] != self.y):
                    self.step += 1
                    self.x = test_player_position[1]
                    self.y = test_player_position[0]
