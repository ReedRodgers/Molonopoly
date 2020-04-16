from InputGenerator import Player, Board, find_all_combos, generate_training_input
from Property import Property
import network
import matplotlib.pyplot as plt

if __name__ == '__main__':
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
            property_list.append(Property(name=name, cost=price, color=col, rent=rent, index=index))
            if colour != col:
                colour = col
                colour_list.append(col)
        return property_list, colour_list


    props, colours = import_properties()

    board = Board(props)
    player1 = Player(920)
    print('finding combos')
    all_combos = find_all_combos(board)
    print('generating input')
    viable_combos = generate_training_input(all_combos, player1.cash)
    print('training models')
    model = network.train(viable_combos, board)
    print('save')
    model.save('heuristic_network')

    plt.figure(figsize=(12, 5))
    # plt.subplot(2, 2, 1)
    # plt.plot(model.history.history['accuracy'], c='k')
    # plt.ylabel('training accuracy')
    # plt.xlabel('epochs')
    # plt.subplot(2, 2, 2)
    plt.plot(model.history.history['loss'], c='b')
    plt.ylabel('training loss (error)')
    plt.title('training')

    # plt.subplot(2, 2, 3)
    # plt.plot(model.history.history['val_accuracy'], c='k')
    # plt.ylabel('testing accuracy')
    # plt.xlabel('epochs')
    # plt.subplot(2, 2, 4)
    plt.plot(model.history.history['val_loss'], c='b')
    plt.ylabel('testing loss (error)')
    plt.title('testing')
    plt.tight_layout()
    plt.show()

