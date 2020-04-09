import itertools
from collections import Counter
'''
This file is responsible for generating input for the NN.
Step 1: evaluate the value of different combinations of properties
'''


class Property:
    def __init__(self, cost, color):
        self.cost = cost
        self.color = color


class Board:
    def __init__(self, properties):
        self.properties = properties
        self.colors = Counter()
        self.color_list = []

    def get_colors(self):
        colors = self.colors
        if len(colors) == 0:
            for prop in self.properties:
                colors.update([prop.color])

        return colors

    def get_color_list(self):
        if len(self.color_list) == 0:
            self.color_list = self.get_colors().keys()
        return self.color_list

class Player:
    def __init__(self, cash):
        self.cash = cash
        self.properties = []


def find_all_combos(board: Board):
    """Given a board, returns all the possible combinations of properties"""
    properties = board.properties
    combos = set()
    for set_size in range(0, len(properties) + 1):
        for combo in itertools.combinations(properties, set_size):
            combos.add(frozenset(combo))
    return combos


def generate_training_input(combos, cash):
    """
    Finds all viable combinations of cash and property for a given player on a given board
    Assumes all viable combos are passed in
    """
    train_input = []
    for combo in combos:
        cost = 0
        too_expensive = False
        for prop in combo:
            cost += prop.cost
            if cost > cash:
                too_expensive = True
                break
        if not too_expensive:
            train_input.append({'cash': cash - cost, 'properties': combo})
    return train_input
