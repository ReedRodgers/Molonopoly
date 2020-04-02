from InputGenerator import Property, Player, Board, find_all_combos, generate_training_input
import network
import matplotlib.pyplot as plt

if __name__ == '__main__':
    pb1 = Property(100, 'b')
    pb2 = Property(100, 'b')
    pb3 = Property(100, 'b')

    py1 = Property(100, 'y')
    py2 = Property(100, 'y')
    py3 = Property(100, 'y')

    pr1 = Property(100, 'r')
    pr2 = Property(100, 'r')
    pr3 = Property(100, 'r')

    props = [pb1, pb2, pb3,
             py1, py2, py3,
             pr1, pr2, pr3]

    board = Board(props)
    player1 = Player(500)
    all_combos = find_all_combos(board)
    viable_combos = generate_training_input(all_combos, player1.cash)
    model = network.train(viable_combos, board)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(model.history.history['accuracy'], c='k')
    plt.ylabel('training accuracy')
    plt.xlabel('epochs')
    plt.subplot(1, 2, 2)
    plt.plot(model.history.history['loss'], c='b')
    plt.ylabel('training loss (error)')
    plt.title('training')

    plt.subplot(1, 3, 1)
    plt.plot(model.history.history['val_accuracy'], c='k')
    plt.ylabel('testing accuracy')
    plt.xlabel('epochs')
    plt.subplot(1, 3, 2)
    plt.plot(model.history.history['val_loss'], c='b')
    plt.ylabel('testing loss (error)')
    plt.title('testing')
    plt.tight_layout()
    plt.show()