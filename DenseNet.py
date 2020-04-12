import tensorflow as tf
import numpy as np
from Player import Player


class DenseNet:

    def __init__(self, name, layers=None):
        self.name = name
        self.layers = layers
        if layers is not None:  # Build a new dense model given different layers
            self.model = False
        else:
            self.load()

    def build_network(self, input_size):
        layers = [tf.keras.layers.Input(shape=(input_size,))]
        for layer in self.layers:
            layers.append(tf.keras.layers.Dense(layer, activation='relu'))
        layers.append(tf.keras.layers.Dense(1, activation='relu'))

        self.model = tf.keras.models.Sequential(layers)
        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=.1), loss='mean_squared_error')

    def predict(self, me: Player, board):
        """Predicts value of possible future board state"""
        board_state = board.get_player_state(me)  # self.arrange_input(me, players, board)  # Generate input

        if not self.model:  # Build model if needed
            self.build_network(len(board_state[0]))

        prediction = self.model.predict(board_state)  # Predict

        return prediction

    def assess(self, me: Player, board):
        """Assesses current board state, and learns from previous assessment"""
        prediction = self.predict(me, board)
        board_state = board.get_player_state(me)
        previous = np.array([[me.value]])
        self.model.train_on_batch(board_state, previous)

        return prediction

    def save(self):
        self.model.save(self.name)

    def load(self):
        self.model = tf.model.load_model(self.name)

    @staticmethod
    def flatten_assets(player, length):
        mtx = np.zeros([length])
        for prop in player.properties:
            mtx[prop.index + 1] = 1

        mtx[0] = player.cash

        return mtx

    # @staticmethod
    # def arrange_input(player, others, board):
    #     # color_counts = board.get_colour_count()
    #     breadth = len(board.properties) + 1
    #     # depth = color_counts.most_common()[0][1]
    #     # colour_list = board.get_colour_list()
    #     # colour_dict = {color: i for i, color in enumerate(colour_list)}
    #     shape = [breadth]
    #
    #     flattened_assets = DenseNet.flatten_assets(player, shape)
    #     for other in others:
    #         assets = DenseNet.flatten_assets(other, shape)
    #         flattened_assets = np.concatenate([flattened_assets, assets])
    #
    #     return flattened_assets
