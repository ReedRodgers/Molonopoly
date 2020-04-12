from queue import Queue as queue
from random import choice
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


def initialize_stage2_game(engines):
    """ Initialize the entire board and first player, as defined in Stage 1"""
    # Generate property list
    property_list, colour_list = import_properties()

    # Create board using the properties provided
    board = Board(property_list, colour_list)

    # Spawn players with money, on the first tile of the board.
    players = queue()

    for i, engine in enumerate(engines):
        new_player = Player(1500, f'Player{i + 1}', engine)
        players.put(new_player)
        board.properties[0].players_present.append(new_player)
    return property_list, board, players


def buy_property(player: Player, others, prop: Property, board):


    if player.decide_purchase(others, prop, board) and player.cash > prop.cost:
        return True
    else:
        return False


def stage2_transactions(player: Player, others, property: Property, board: Board):
    """ In stage 2: there are two players """
    if not property.owner:  # if the property doesn't have an owner
        # Determine whether or not to buy the property
        if buy_property(player, others, property, board):
            player.purchase(property)  # Buy the property if NN says you should buy it
    else:
        payable_rent = property.determine_rent(player, board.colour_counts)  # Determine amount of payable rent
        player.pay_rent(property, board.colour_counts)  # shouldn't make a difference if the player pays rent to himself
    return None


def get_players(player_queue: queue):

    # Copy queue members (O(1) time)
    p1 = player_queue.get()
    p2 = player_queue.get()

    # Put back in queue (O(1))
    player_queue.put(p1)
    player_queue.put(p2)
    return p1, p2


def generate_log(player1: Player, player2: Player):
    return f'{player1.position}, {player1.cash}, {player1.get_property_indices()}, ' \
           f'{player2.position}, {player2.cash}, {player2.get_property_indices()}'


def run_game(file_handle, game_board: Board, players: queue, rounds_per_game=300):
    turns = 0

    # Get handles to the players of the game
    person1, person2 = get_players(players)

    # First log to describe initial state
    file_handle.write(generate_log(player1=person1, player2=person2) + "\n")

    while turns < rounds_per_game * players.qsize():
        # Who's turn is it?
        current_player = players.get()

        # Roll the dice, and move the player accordingly
        current_position = game_board.roll(current_player)
        current_property = game_board.properties[current_position]

        # Make transaction decisions
        p2 = players.get()
        stage2_transactions(current_player, [p2], current_property, game_board)
        players.put(p2)

        # If player runs out of money while paying rent, game is over.
        if current_player.cash < 0:
            # Log the results of the turn
            file_handle.write(generate_log(player1=person1, player2=person2) + "\n")
            person1.final_training([person2], game_board, turns)
            person2.final_training([person1], game_board, turns)
            person2.network.save()
            return None

        # Add the player to the end of the queue
        players.put(current_player)

        # Log the results of the turn
        file_handle.write(generate_log(player1=person1, player2=person2) + "\n")

        # Mark turn as done
        turns += 1


def logged_simulation(file_handle):
    # Initialize board
    network = DenseNet('first_try', [56, 20, 2])
    engines = [network, network]
    properties, new_board, player_list = initialize_stage2_game(engines)

    # Run game
    run_game(file_handle, new_board, players=player_list)
    return None


if __name__ == '__main__':
    # For benchmarking purposes
    t0 = time()
    runs = 1000

    # Generate a UUID to avoid overwriting files that trained different NNs.
    output_file = "MoloSim_" + uuid4().hex[:5] + ".csv"
    with open(output_file, "w") as f:
        # Write header labels
        f.write("P1_Pos, P1_Cash, P1_Props, P2_Pos, P2_Cash, P2_Props" + "\n")

        # Run all the requested simulations
        for n in range(runs):
            # Mark that a new game is about to be loaded
            f.write("=====" * 10 + " Simulated Game #{} ".format(n) + "=====" * 10 + "\n")
            logged_simulation(f)

        f.write("====" * 10 + f'END OF REQUESTED SIMULATIONS; N = {runs}, elapsed_time = {time() - t0}')
        f.write("\n")

