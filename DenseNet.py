from Network import Network
from Board import Board
import tensorflow as tf


class DenseNet(Network):

    def __init__(self, name, layers=None):
        self.previous = False
        self.name = name
        self.layers = layers
        if layers is not None:  # Build a new dense model given different layers
            self.model = False
        else:
            self.load()

    def loss(self, prediction):
        if not self.previous:
            return 0
        return (self.previous - prediction) ** 2

    def build_network(self, input_size):
        layers = [tf.keras.layers.Input(shape=(input_size,))]
        for layer in self.layers:
            layers.append(tf.keras.layers.Dense(layer, activation='relu'))
        layers.append(tf.keras.layers.Dense(1, activation='relu'))

        self.model = tf.keras.models.Sequential(layers)
        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=.1), loss=self.loss)

    def predict(self, players, me, board: Board):
        board_state = Network.arrange_input(me, players, board)
        if not self.model:
            self.build_network(len(board_state))
        prediction = self.model.predict(board_state)
        self.learn(board_state)
        self.previous = prediction
        return prediction

    def learn(self, board_state):
        self.model.train_on_batch(board_state)

    def save(self):
        self.model.save(self.name)

    def load(self):
        self.model = tf.model.load_model(self.name)
