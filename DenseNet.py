from Network import Network
from InputGenerator import Board

class DenseNet(Network):

    def __init__(self, name, layers):
        self.previous = None
        self.name = name
        self.version = self.name + '.csv'
        self.layers = layers
        self.net = False

    def build_network(self, input_size):



    def predict(self, players, me, board: Board):
        board_state = Network.arrange_input(me, players, board)