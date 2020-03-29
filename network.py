from InputGenerator import Board, generate_training_input, find_all_combos, Player
import numpy as np
from collections import Counter

def read_board(combos, board: Board):
    """Given property cash combos from InputGenerator, return array datatype for learning"""
    color_counts = board.get_colors()
    breadth = len(color_counts)
    depth = color_counts.most_common()[0][1]
    color_list = board.get_color_list()
    color_dict = {color: i for i, color in enumerate(color_list)}
    data = []
    for combo in combos:
        mtx = np.zeros([breadth, depth], dtype=int)
        color_count = Counter(color_list)
        color_count.subtract(color_list)
        for prop in combo['properties']:
            color = prop.color
            mtx[color_dict[color], color_count[color]] = 1
            color_count.update([color])
        cash = np.array([combo['cash']])
        ls = mtx.flatten()
        data.append(np.concatenate((cash, ls)))

    return data


def evaluate_property(prop_set, board_count):
    """Evaluates value of a set of properties given the total properties on the board"""
    prop_counter = Counter()
    prop_value = Counter()
    for prop in prop_set:
        prop_counter.update(prop.color)
        prop_value.update({prop.color: prop.cost})
    total_value = 0
    for color in prop_value.keys():
        if prop_counter[color] == board_count[color]:
            prop_value.update({color: prop_value[color]})
        total_value += prop_value[color]
    return total_value


def evaluate_heuristic(input, board: Board):
    """return heuristic value of property cash combination"""
    property_value = evaluate_property(input['properties'], board.get_colors())
    return property_value


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