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
    def __init__(self, cash, properties):
        self.cash = cash
        self.properties = properties


'''Given a board, returns all the possible combinations of properties'''
def find_all_combos(board: Board):
    return [[]]

'''Finds all viable combinations of cash and property for a given player on a given board'''
def generate_training_input(board: Board, player: Player):
    return [{'cash': 0,
             'properties': [Property(0, 'blue')]
             }]
