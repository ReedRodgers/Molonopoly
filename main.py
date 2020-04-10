import Board
from queue import Queue as queue
from random import choice
from time import time
from uuid import uuid4

import Player
import Property


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
        property_list.append(Property.Property(name=name, cost=price, colour=col, rent=rent, index=index))
        if colour != col:
            colour = col
            colour_list.append(col)
    return property_list


def initialize_stage2_game(player_count=2):
    """ Initialize the entire board and first player, as defined in Stage 1"""
    # Generate property list
    property_list, colour_list = import_properties()

    # Create board using the properties provided
    board = Board.Board(property_list, colour_list)

    # Spawn players with money, on the first tile of the board.
    players = queue()
    for i in range(player_count):
        new_player = Player.Player(cash=1500, identifier=f'Player{i + 1}')
        players.put(new_player)
        board.properties[0].players_present.append(new_player)
    return property_list, board, players


def buy_property(player: Player.Player, others, property: Property.Property, board):
    """Put the Network here"""
    player.decide_purchase(others, property, board)
    if choice([0, 1]) and player.cash > property.cost:
        return True
    else:
        return False


def stage2_transactions(player: Player.Player, property: Property.Property, board : Board.Board):
    """ In stage 2: there are two players """

    # Determine amount of payable rent
    payable_rent = property.determine_rent(player, board.colour_counts)

    if not property.owner:  # if the property doesn't have an owner
        # Determine whether or not to buy the property
        if buy_property(player, property, rent=payable_rent):
            player.purchase(property)  # Buy the property if NN says you should buy it
    else:
        player.pay_rent(fee=payable_rent)  # shouldn't make a difference if the player pays rent to himself
    return None


def get_players(player_queue: queue):
    # Copy queue members (O(1) time)
    p1 = player_queue.get()
    p2 = player_queue.get()

    # Put back in queue (O(1))
    player_queue.put(p1)
    player_queue.put(p2)
    return p1, p2


def generate_log(player1: Player.Player, player2: Player.Player):
    return f'{player1.position}, {player1.cash}, {player1.get_property_indices()}, ' \
           f'{player2.position}, {player2.cash}, {player2.get_property_indices()}'


def run_game(file_handle, game_board: Board.Board, players: queue, rounds_per_game=1000):
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
        stage2_transactions(current_player, current_property, game_board)

        # If player runs out of money while paying rent, game is over.
        if current_player.cash < 0:
            # Log the results of the turn
            file_handle.write(generate_log(player1=person1, player2=person2) + "\n")
            return None

        # Add the player to the end of the queue
        players.put(current_player)

        # Log the results of the turn
        file_handle.write(generate_log(player1=person1, player2=person2) + "\n")

        # Mark turn as done
        turns += 1


def logged_simulation(file_handle):
    # Initialize board
    properties, new_board, player_list = initialize_stage2_game()

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

