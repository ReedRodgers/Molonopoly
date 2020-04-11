from collections import Counter
from random import randint


class Board:
    def __init__(self, properties, colour_list):
        self.properties = properties  # List with objects of type: Property

        # Store these variables so that they're not evaluated multiple times
        self.property_count = len(properties)
#        self.unowned = dict()
        self.colour_counts = Counter()
        self.colour_list = colour_list  # Stores ordered list of colours to maintain order for learning input

#         for idx, prop in enumerate(self.properties):
#            self.unowned[idx] = True

    def get_colour_count(self):
        colours = self.colour_counts
        if len(colours) == 0:
            for prop in self.properties:
                colours.update([prop.colour])

        return colours

    def get_colour_list(self):
        return self.colour_list


    def debug(self):
        """Print out every single square on the board, if it's owned, if there's a player on that square"""
        for square in self.properties:
            print(f'{square}; owner={square.owner}; players_present={square.players_present}')

    def roll(self, player):
        current_position = player.position
        dice_roll = randint(1, 7) + randint(1, 7)

        # Use modulus to ensure circular behaviour
        new_position = (current_position + dice_roll) % self.property_count

        # Remove player from old position
        self.properties[current_position].players_present.remove(player)

        # Change player's position
        player.position = new_position
        self.properties[new_position].players_present.append(player)

        return new_position

    def get_unowned_properties(self):
        """ Abandoned because of unreasonable time complexity, even with the dictionary"""
        pass