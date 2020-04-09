"""
This file is responsible for generating input for the NN.
Step 1: evaluate the value of different combinations of properties
"""
from random import randint


rent_check = {'Purple': 2, 'Light-Blue': 3, 'Violet': 3,
              'Orange': 3, 'Yellow': 3, 'Red': 3,
              'Dark-Green': 3, 'Dark-Blue': 2}


class Square:
    def __init__(self):
        self.colour = "BLACK"
        self.players_present = []

    def __repr__(self):
        return "CornerSquare"

    def __str__(self):
        return "CornerSquare"


class Property(Square):
    def __init__(self, cost: int, colour: str, rent: int, name: str):
        self.cost = int(cost)
        self.colour = colour
        self.rent = int(rent)
        self.name = name
        self.owner = False
        self.players_present = []

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'

    def determine_rent(self, landing_player):
        # if the property isn't owned by anyone, rent would be normal priced
        if not self.owner:
            return self.rent
        elif self.owner is landing_player:  # if property is owned by the player who lands on it, no rent.
            """ This may be pointless- this should never arise given the logic of stage2_transactions()"""
            return 0
        else:  # property is owned by the opponent
            if not self.owner.properties:  # owner has no properties
                return self.rent
            else:
                counter = 0
                for prop in self.owner.properties:
                    if prop.colour == self.colour:
                        counter += 1
                if counter == rent_check[self.colour]:
                    return self.rent * 2
                else:
                    return self.rent


class Board:
    def __init__(self, properties):
        self.full_board = properties  # List with objects of type: Property
        self.property_count = len(properties)  # Store this variable so that it's not evaluated multiple times.

    def debug(self):
        """Print out every single square on the board, if it's owned, if there's a player on that square"""
        for square in self.full_board:
            print(f'{square}; owner={square.owner}; players_present={square.players_present}')

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
    def __init__(self, cash, identifier):
        self.name = identifier
        self.cash = int(cash)
        self.properties = []   # Perhaps this should be a dictionary, with 4 keys corresponding to the colours
        self.position = 0

    def purchase(self, some_property: Property):
        self.cash -= some_property.cost
        self.properties.append(some_property)
        some_property.owner = self

    def pay_rent(self, fee: int):
        self.cash -= int(fee)

    def valuate(self):
        # Account for cash
        net_worth = self.cash

        # Account for property value(s)
        for prop in self.properties:
            net_worth += prop.cost
        return net_worth

    def __repr__(self):
        return f'{self.name}: ({self.cash}, {self.valuate()})'

    def __str__(self):
        return f'{self.name}'
