from InputGenerator import Board, generate_training_input, find_all_combos, Player
import numpy as np

def read_board(combos, board: Board):
    """Given property cash combos from InputGenerator, return array datatype for learning"""
    colors = board.get_colors()
    breadth = len(colors)
    depth = colors.most_common()[0][1]
    data = []
    for combo in combos:
        mtx = np.zeros([depth, breadth], dtype=int)
    return []

def evaluate_heuristic(input, output):
    """return heuristic value of property cash combination"""
    return 0


def apply_heuristic(x_values):
    """
    return training values for property combinations by feeding them to the heuristic
    Accepts a list of cash value and property dictionaries
    """
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