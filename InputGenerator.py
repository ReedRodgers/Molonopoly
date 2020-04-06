"""
This file is responsible for generating input for the NN.
Step 1: evaluate the value of different combinations of properties
"""
from random import randint

class Square:
    def __init__(self):
        self.colour = "BLACK"
        self.players_present = []

    def __repr__(self):
        return "CornerSquare"

    def __str__(self):
        return "CornerSquare"


class Property(Square):
    def __init__(self, cost, colour, rent, name):
        self.cost = cost
        self.colour = colour
        self.rent = rent
        self.name = name
        self.owner = False
        self.players_present = []

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'


class Board:
    def __init__(self, properties):
        self.full_board = properties  # List with objects of type: Property
        self.property_count = len(properties)  # Store this variable so that it's not evaluated multiple times.

    def debug(self):
        """Print out every single square on the board, if it's owned, if there's a player on that square"""
        for square in self.full_board:
            print(f'{square}; owned={square.owned_by}; players_present={square.players_present}')

    def roll(self, player):
        current_position = player.position
        dice_roll = randint(0, 7)

        # Use modulus to ensure circular behaviour
        new_position = (current_position + dice_roll) % self.property_count

        # Remove player from old position
        self.full_board[current_position].players_present.remove(player)

        # Change player's position
        player.position = new_position
        self.full_board[new_position].players_present.append(player)

        return new_position


class Player:
    def __init__(self, cash):
        self.cash = cash
        self.properties = []   # Perhaps this should be a dictionary, with 4 keys corresponding to the colours
        self.position = 0

    def purchase(self, some_property: Property):
        self.cash -= some_property.cost
        self.properties.append(some_property)
        some_property.owner = self


