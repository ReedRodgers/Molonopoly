def read_board(property_combos):
    """Given property cash combos from InputGenerator, return array datatype for learning"""
    return []


def evaluate_heuristic(property_ownership, output):
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
