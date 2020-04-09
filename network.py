class network:

    def __init__(self, net, name):
        self.net = net
        self.previous = None
        self.name = name

    def load_from_weights(self):
        """Read in weight csv file"""

    def predict(self, players, me):
        """Given a list of players, and an identifier of which player is represented by the net,
        return the expected value of the board"""

    def learn(self, prev, curr):
        """applies learning by comparing previous estimate to current estimate"""

    def save(self):
        """saves weights as .csv"""









def read_board(property_combos):
    """Given property cash combos from InputGenerator, return array datatype for learning"""
    return []


def train(property_combos):
    """
    Entry point method to be called from main.
    Accepts property combinations, processes them, and trains the model
    """
    x_values = read_board(property_combos)
    y_values = apply_heuristic(x_values)


def predict(property_combo):
    return 0
