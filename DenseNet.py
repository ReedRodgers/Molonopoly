from Board import Board
import tensorflow as tf
import numpy as np
from collections import Counter
from Player import Player


class DenseNet:

    def __init__(self, name, layers=None):
        self.name = name
        self.layers = layers
        if layers is not None:  # Build a new dense model given different layers
            self.model = False
        else:
            self.load()
        self.previous = False

    # def loss(self, prediction, previous):
    #     if not self.previous:
    #         return 0.0
    #     return (self.previous - prediction) ** 2

    def build_network(self, input_size):
        layers = [tf.keras.layers.Input(shape=(input_size,))]
        for layer in self.layers:
            layers.append(tf.keras.layers.Dense(layer, activation='relu'))
        layers.append(tf.keras.layers.Dense(1, activation='relu'))

        self.model = tf.keras.models.Sequential(layers)
        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=.1), loss='mean_squared_error')

    def predict(self, players, me, board: Board):  # assesses future state
        board_state = self.arrange_input(me, players, board)  # Generate input

        if not self.model:  # Build model if needed
            self.build_network(len(board_state))

        prediction = self.model.predict(np.array([list(board_state)]))  # Predict

        return prediction

    def assess(self, players, me: Player, board: Board):  # Assess current board state and learns from previous assessment
        prediction = self.predict(players, me, board)
        board_state = self.arrange_input(me, players, board)

        self.previous = np.array([[me.value]])
        board_state = np.array([list(board_state)])
        self.model.train_on_batch(board_state, self.previous)

        return prediction

    def save(self):
        self.model.save(self.name)

    def load(self):
        self.model = tf.model.load_model(self.name)

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

        flattened_assets = DenseNet.flatten_assets(player, shape, colour_dict)
        for other in others:
            assets = DenseNet.flatten_assets(other, shape, colour_dict)
            flattened_assets = np.concatenate([flattened_assets, assets])

        return flattened_assets
