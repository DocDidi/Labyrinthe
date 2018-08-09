#! /usr/bin/env python3
# coding: utf-8

from Fonctions.Variables import *


class Minotaur:
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.target = (x, y)

    def display(self, margin, margin_v):
        color = B_GREEN_TEXT
        print(
            "{0}\033[{1};{2}H{3}".format(
                color,
                self.y + margin_v,
                self.x+1+margin,
                SYMBOL_PLAYER) +
            CLR_ATTR)

    def move(self, movement, props, width):
        """Move the player"""
        width = width + 1
        test_minotaur_position = [self.y, self.x]
        if movement == "U":
            test_minotaur_position = [self.y - 1, self.x]
            test_item = props[(self.y - 1) * width + self.x]
        elif movement == "D":
            test_minotaur_position = [self.y + 1, self.x]
            test_item = props[(self.y + 1) * width + self.x]
        elif movement == "R":
            test_minotaur_position = [self.y, self.x + 1]
            test_item = props[(self.y) * width + self.x + 1]
        elif movement == "L":
            test_minotaur_position = [self.y, self.x - 1]
            test_item = props[(self.y) * width + self.x - 1]

        block = False
        if test_item.block:
            block = True
        if not block:
            if (
                    (test_minotaur_position[1] != self.x) or
                    (test_minotaur_position[0] != self.y)):
                self.x = test_minotaur_position[1]
                self.y = test_minotaur_position[0]
