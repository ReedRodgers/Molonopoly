"""
This file is responsible for generating input for the NN.
Step 1: evaluate the value of different combinations of properties
"""


class Square:
    def __init__(self):
        self.colour = "BLACK"
        self.players_present = []

    def __repr__(self):
        return "CornerSquare"

    def __str__(self):
        return "CornerSquare"


class Property(Square):
    def __init__(self, cost, colour, index):
        self.cost = cost
        self.colour = colour
        self.index = index
        self.under_management = False
        self.players_present = []

    def __str__(self):
        return f'{self.colour}{self.index}'

    def __repr__(self):
        return f'{self.colour}{self.index}'


class Board:
    def __init__(self, properties,  colours):
        self.colours = colours
        self.properties = properties

        self.full_board = []
        for idx, prop in enumerate(properties):
            if idx % (len(properties) / len(colours)) == 0:
                self.full_board.append(Square())
            self.full_board.append(prop)
        # assert self.full_board.count(Square()) == 4, "Board is not a square"

    def debug(self):
        """Print out every single square on the board, if it's owned, if there's a player on that square"""
        for square in self.full_board:
            if type(square) == Property:
                print(f'{square}; owned={square.under_management}; players_present={square.players_present}')
            else:
                print(f'{square}; players_present={square.players_present}')

    def roll(self):
        pass


class Player:
    def __init__(self, cash, starting_position):
        self.cash = cash
        self.properties = []   # Perhaps this should be a dictionary, with 4 keys corresponding to the colours
        self.position = starting_position

    def purchase(self, some_property: Property):
        self.cash -= some_property.cost
        self.properties.append(some_property)
        some_property.under_management = True


def find_all_combos(board: Board, player: Player):
    """Given a board, returns all the possible combinations of properties"""
    unclaimed_properties = [i for i in board.properties if i.under_management is False]
    owned_properties = player.properties
    purchases_possible = player.cash/100
    return [[]]


def generate_training_input(combos, player: Player):
    """Finds all viable combinations of cash and property for a given player on a given board"""
    return [{'cash': 0,
             'properties': [Property(0, 'blue')]
             }]
