import InputGenerator
import network
from queue import Queue as queue


def read_properties():
    """Generator function to read from csv"""
    with open("property_list.csv", "r", encoding="utf-8-sig") as f:
        yield from f


def import_properties():
    property_list = []
    data = read_properties()
    for entry in data:
        name, price, rent, col = entry.strip().split(",")
        property_list.append(InputGenerator.Property(name=name, cost=price, colour=col, rent=rent))
    return property_list


def initialize_stage2_game(player_count=1):
    """ Initialize the entire board and first player, as defined in Stage 1"""

    # Generate property list
    property_list = import_properties()

    # Create board using the properties provided
    board = InputGenerator.Board(property_list)

    # Spawn players with money, on the first tile of the board.
    players = queue()
    for _ in range(player_count):
        new_player = InputGenerator.Player(cash=1500)
        players.put(new_player)
        board.full_board[0].players_present.append(new_player)
    return property_list, board, players


def buy_property(player: InputGenerator.Player, property: InputGenerator.Property, rent: int):
    """Put the Network here"""
    if rent > 20:
        return True
    else:
        return False


def stage2_transactions(player: InputGenerator.Player, property: InputGenerator.Property):
    """ In stage 2, the player can either buy a property, or will have to pay rent for it."""

    if not property.owner:

        # Determine amount of rent payable
        payable_rent = property.determine_rent(player)

        # Determine whether or not to buy the property
        if buy_property(player, property, rent=payable_rent):
            player.purchase(property)  # Buy the property if NN says you should buy it
        else:
            player.pay_rent(fee=payable_rent)  # Pay the rent if NN says it's not worth buying
    return None


def run_game(game_board: InputGenerator.Board, players: queue, rounds_per_game=25):
    turns = 0
    while turns < rounds_per_game * players.qsize():
        # Who's turn is it?
        current_player = players.get()

        # Roll the dice, and move the player accordingly
        current_property = game_board.full_board[game_board.roll(current_player)]

        # Make transaction decisions
        stage2_transactions(player=current_player, property=current_property)

        # Add the player to the end of the queue
        players.put(current_player)

        # Mark turn as done
        turns += 1


if __name__ == '__main__':

    # Initialize board
    properties, new_board, player_list = initialize_stage2_game()

    # Ensure board is setup properly
    new_board.debug()

    # Run game
    run_game(new_board, players=player_list)

    # Determine winner(s)
    max_value = 0
    for _ in range(player_list.qsize()):
        player = player_list.get()
        worth = player.valuate()
        if worth > max_value:
            max_value = worth
            winner = player
    print(f'And the winner is: {player}, who finished the game with: ${player.valuate()}')

