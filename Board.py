from collections import Counter
from random import randint
from Player import Player
from DenseNet import DenseNet
from Property import Property
from Game import Game
import numpy as np


class Board:
    def __init__(self, properties, colour_list, players):
        self.properties = properties  # List with objects of type: Property
        self.players = players

        # Store these variables so that they're not evaluated multiple times
        self.property_count = len(properties)
        self.colour_counts = Counter()
        self.colour_list = colour_list  # Stores ordered list of colours to maintain order for learning input
        self.starting_cash = players[0].cash

        self.player_state = False
        self.player_order = False
        self.asset_length = 0  # Length of a single players state

    def get_colour_count(self):
        """Deprecated: returns a counter of the number of properties of each color"""
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
        """Rolls dice and moves player"""
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

    def build_player_state(self):
        """Generates the initial board state for each player, representing their cash and property assets"""
        self.asset_length = len(self.properties) + 1
        self.player_state = {}
        player_state = {}
        for player in self.players:
            player_state[player.name] = DenseNet.flatten_assets(player, self.asset_length)

        for player in self.players:
            concat_list = [0] * len(self.players)
            for opponent in self.players:
                concat_list[self.get_player_order(player, opponent)] = player_state[opponent.name]
            self.player_state[player.name] = np.array([np.concatenate(concat_list)])

    def get_player_state(self, player: Player):
        """returns board state for a given player"""
        if not self.player_state:
            self.build_player_state()
        return self.player_state[player.name]

    def get_player_order(self, p1, p2):
        """returns index of p2 relative to p1"""
        if not self.player_order:
            self.player_order = {player.name: i for i, player in enumerate(self.players)}

        p1 = self.player_order[p1.name]
        p2 = self.player_order[p2.name]

        if p1 <= p2:
            return p2 - p1
        if p1 > p2:
            return len(self.players) - p1 + p2

    def get_property_index(self, prop: Property, player: Player):
        """returns index of prop in the player_state for player"""
        order = self.get_player_order(player, prop.owner)
        return order * self.asset_length + prop.index + 1

    def get_cash_index(self, p1: Player, p2: Player):
        """Returns index of p2's cash in p1's player_state"""
        order = self.get_player_order(p1, p2)
        return order * self.asset_length

    def deposit(self, amount, account: Player):
        """Adds a (possibly negative) sum of money to a player's account and updates player_state for each player"""
        account.cash += amount
        for player in self.players:
            self.get_player_state(player)[0][self.get_cash_index(player, account)] = account.cash

    def move_property(self, prop: Property, benefactor: Player, give: int):
        """Adds a property to a player's account and updates player_state for each player"""
        if give > 0:
            benefactor.properties.append(prop)
            prop.owner = benefactor
            for player in self.players:
                self.get_player_state(player)[0][self.get_property_index(prop, player)] = give
        else:
            for player in self.players:
                self.get_player_state(player)[0][self.get_property_index(prop, player)] = give
            benefactor.properties.remove(prop)
            prop.owner = False

    def land(self, prop, player):
        if not prop.owner:  # if the property doesn't have an owner
            # Determine whether or not to buy the property
            if player.decide_purchase(prop, self):
                player.purchase(prop)  # Buy the property if NN says you should buy it

        else:
            rent = prop.determine_rent(player, self.colour_counts)  # Determine amount of payable rent
            self.deposit(0 - rent, player)  # shouldn't make a difference if the player pays rent to himself
            self.deposit(rent, prop.owner)

    def reset(self):
        self.player_state = False
        self.player_order = False

        for player in self.players:
            player.properties = []
            player.cash = self.starting_cash
            player.position = -1

        for prop in self.properties:
            prop.owner = False
            prop.players_present = []

        self.properties[-1].players_present = [player for player in self.players]

    def play(self, max_cycles, file):
        game = Game(file)

        for cycle in range(max_cycles):

            for player in self.players:
                position = self.roll(player)
                prop = self.properties[position]
                self.land(prop, player)

                line = f'{cycle}.\t'
                for p in self.players:
                    line = line + f'{p.position} \t {p.cash} \t {p.get_property_indices()} \t || \t'
                game.record(line)

                if player.cash < 0:
                    for player in self.players:
                        player.final_training(self, cycle)

                    self.reset()
                    game.write()
                    return None

