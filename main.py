import InputGenerator
import network

if __name__ == '__main__':
    prop1 = InputGenerator.Property(100, 'blue')
    board = InputGenerator.Board([prop1])
    player1 = InputGenerator.Player(500)
    all_combos = InputGenerator.find_all_combos(board)
    viable_combos = InputGenerator.generate_training_input(all_combos, player1)
    network.train(viable_combos)