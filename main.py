import InputGenerator
import network


def initialize_stage1_game(property_colours=['red', 'blue', 'green', 'purple'],
                           property_per_colour=5, cost_per_property=100):
    """ Initialize the entire board and first player, as defined in Stage 1"""

    # Generate property list
    property_list = [InputGenerator.Property(cost_per_property, colour, i)
                     for colour in property_colours for i in range(property_per_colour)]

    board = InputGenerator.Board(property_list, property_colours)
    player1 = InputGenerator.Player(property_per_colour * cost_per_property, board.full_board[0])
    board.full_board[0].players_present.append('player1')
    return property_list, board, player1


if __name__ == '__main__':

    # Initialize board
    properties, new_board, main_player = initialize_stage1_game()

    # Ensure board is setup properly
    new_board.debug()

    # Get all combinations
    all_combos = InputGenerator.find_all_combos(new_board)

    # Discern viable combinations
    viable_combos = InputGenerator.generate_training_input(all_combos, main_player)

    # Train network
    network.train(viable_combos)