from InputGenerator import Board, generate_training_input, find_all_combos, Player
import numpy as np
from collections import Counter
from copy import deepcopy
import tensorflow as tf
from random import sample
import math

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


def evaluate_options(properties, cash, remaining_properties, color_distribution):
    """Evaluates value of cash based on which properties could be purchased with it"""
    value = 0  # Approximate value of each option evaluated so far
    options = 0  # Number of options evaluated so far
    can_buy = False
    properties = list(properties)

    while len(remaining_properties) > 0:
        prop = remaining_properties.pop()
        if prop.cost > cash:
            continue
        can_buy = True
        properties.append(prop)
        v, o = evaluate_options(properties, cash - prop.cost, deepcopy(remaining_properties), color_distribution)
        properties.pop()
        value += v
        options += o

    if not can_buy:
        value = evaluate_property(properties, color_distribution)
        options = 1

    return value, options


def evaluate_heuristic(input, board: Board):
    """return heuristic value of property cash combination"""
    owned_properties = input['properties']
    property_value = evaluate_property(owned_properties, board.get_colors())
    remaining_properties = set(board.properties) - set(owned_properties)
    value, options = evaluate_options(owned_properties, input['cash'], remaining_properties, board.get_colors())
    return property_value + value / options


def apply_heuristic(x_values, board: Board):
    """
    return training values for property combinations by feeding them to the heuristic
    Accepts a list of cash value and property dictionaries
    """
    evaluations = []
    for combo in x_values:
        evaluations.append(evaluate_heuristic(combo, board))
    return evaluations


def loss(y_true, y_predict):
    return (y_true - y_predict)**2

# def accuracy(y_true, y_predict):
#     return math.log(1/abs(y_true - y_predict), 10)


def train(property_combos, board: Board):
    """
    Entry point method to be called from main.
    Accepts property combinations, processes them, and trains the model
    """
    combo_count = len(property_combos)
    training = sample(range(combo_count), math.floor(combo_count*.75))
    testing = list(set(range(combo_count)) - set(training))
    training_combos = [property_combos[i] for i in training]
    testing_combos = [property_combos[i] for i in testing]

    print('converting combos to input')
    x_train = read_board(training_combos, board)
    print('applying heuristic to combos')
    y_train = apply_heuristic(training_combos, board)

    print('the same but for testing')
    x_test = read_board(testing_combos, board)
    y_test = apply_heuristic(testing_combos, board)

    color_counts = board.get_colors()
    breadth = len(color_counts)
    depth = color_counts.most_common()[0][1]
    print('create model')
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(breadth * depth + 1,)),
        tf.keras.layers.Dense(breadth + depth, activation='relu'),
        tf.keras.layers.Dense(breadth + 1, activation='relu'),
        tf.keras.layers.Dense(1, activation='relu')
    ])
    print('compile')
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=.1),
                  loss=loss#,
                  # metrics=[accuracy]
                  )
    print('fit')
    model.fit(np.array(x_train), np.array(y_train), epochs=25, validation_data=(np.array(x_test), np.array(y_test)))

    return model


def predict(property_combo):
    return 0