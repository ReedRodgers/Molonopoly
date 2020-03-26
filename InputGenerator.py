import itertools
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
    """Finds all viable combinations of cash and property for a given player on a given board"""

