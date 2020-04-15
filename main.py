from Heuristic import Heuristic
from matplotlib import pyplot as plt
from Logger import Logger
from time import time
from uuid import uuid4

from Board import Board
from Player import Player
from Property import Property
from DenseNet import DenseNet

def read_properties():
    """Generator function to read from csv"""
    with open("property_list.csv", "r", encoding="utf-8-sig") as f:
        yield from f


def import_properties():
    property_list = []
    colour_list = []
    data = read_properties()
    colour = ''
    for index, entry in enumerate(data):
        name, price, rent, col = entry.strip().split(",")
        property_list.append(Property(name=name, cost=price, colour=col, rent=rent, index=index))
        if colour != col:
            colour = col
            colour_list.append(col)
    return property_list, colour_list


def initialize_board(engines, loggers, cash=1500):
    """ Initialize the entire board and first player, as defined in Stage 1"""
    # Generate property list
    property_list, colour_list = import_properties()

    # Spawn players with money, on the first tile of the board.
    players = []

    for i, engine, logger in zip(range(len(engines)), engines, loggers):
        new_player = Player(cash, f'Player{i + 1}', engine, logger)
        players.append(new_player)
        property_list[-1].players_present.append(new_player)

    # Create board using the properties provided
    return Board(property_list, colour_list, players)


if __name__ == '__main__':
    # For benchmarking purposes
    t0 = time()
    runs = 500

    #Define decision making engines to power players
    # network1 = DenseNet('second_try')#, [28, 2]
    network1 = Heuristic()
    network2 = DenseNet('first_try')#, [56, 28, 2]
    engines = [network1, network2]

    p1_logger = Logger()
    p2_logger = Logger()
    loggers = [p1_logger, p2_logger]

    # Create board using the properties provided
    board = initialize_board(engines, loggers)

    # Generate a UUID to avoid overwriting files that trained different NNs.
    output_file = "MoloSim_" + uuid4().hex[:5] + ".csv"
    with open(output_file, "w") as f:
        # Write header labels
        f.write("P1_Pos, P1_Cash, P1_Props, P2_Pos, P2_Cash, P2_Props" + "\n")

        # Run all the requested simulations
        for n in range(runs):
            # Mark that a new game is about to be loaded
            f.write('\n' + "=====" * 10 + " Simulated Game #{} ".format(n) + "=====" * 10 + "\n")
            board.play(500, f)

        f.write("====" * 10 + f'END OF REQUESTED SIMULATIONS; N = {runs}, elapsed_time = {time() - t0}')
        f.write("\n")

    for i, player in enumerate(board.players):

        player.network.save()
        results = player.logger.per_turn_metrics

        ax1 = plt.subplot(len(board.players), 3, i * 3 + 1)
        ax1.set_title(player.name + ' loss')
        ax1.plot(results['loss'])

        ax2 = plt.subplot(len(board.players), 3, i * 3 + 2)
        ax2.set_title(player.name + ' value')
        ax2.plot(results['value'])

        ax3 = plt.subplot(len(board.players), 3, i * 3 + 3)
        ax3.plot(results['properties'])
        ax3.set_title(player.name + ' properties')

    plt.show()

    for i, player in enumerate(board.players):

        results = player.logger.game_metrics

        ax1 = plt.subplot(len(board.players), 3, i * 3 + 1)
        ax1.set_title(player.name + ' loss')
        ax1.plot(results['loss'])

        ax2 = plt.subplot(len(board.players), 3, i * 3 + 2)
        ax2.set_title(player.name + ' value')
        ax2.plot(results['value'])

        ax3 = plt.subplot(len(board.players), 3, i * 3 + 3)
        ax3.set_title(player.name + ' assessment')
        ax3.plot(results['assessment'])

    plt.show()
