from Board import Board
import numpy as np
from collections import Counter


class Network:

    def __init__(self, name):
        self.name = name
        self.version = self.name + '.csv'

    # def get_file_name(self):
    #     """To be filled in in more detail if we decide on more complex network versioning"""
    #     if not self.version:
    #         self.version = self.name + '.csv'
    #     return self.version


    def load(self):
        """Read in weight csv file"""

    def predict(self, players, me, board: Board):
        """Given a list of players, and an identifier of which player is represented by the net,
        return the expected value of the board"""

        return 0

    def save(self):
        """saves weights as .csv"""


    @staticmethod
    def flatten_assets(player, shape, colour_dict):
        mtx = np.zeros(shape)
        colour_count = Counter()
        for prop in player.properties:
            colour = prop.colour
            colour_count.update(colour)
            mtx[colour_dict[colour], colour_count[colour] - 1] = 1

        cash = np.array([player.cash])
        mtx = mtx.flatten()

        return np.concatenate([cash, mtx])

    @staticmethod
    def arrange_input(player, others, board):
        color_counts = board.get_colour_count()
        breadth = len(color_counts)
        depth = color_counts.most_common()[0][1]
        colour_list = board.get_colour_list()
        colour_dict = {color: i for i, color in enumerate(colour_list)}
        shape = [breadth, depth]

        flattened_assets = Network.flatten_assets(player, shape, colour_dict)
        for other in others:
            assets = Network.flatten_assets(other, shape, colour_dict)
            np.concatenate([flattened_assets, assets])

        return flattened_assets
