import InputGenerator
import network
import matplotlib.pyplot as plt

if __name__ == '__main__':
    prop1 = InputGenerator.Property(100, 'blue')
    board = InputGenerator.Board([prop1])
    player1 = InputGenerator.Player(500)
    all_combos = InputGenerator.find_all_combos(board)
    viable_combos = InputGenerator.generate_training_input(all_combos, player1.cash)
    model = network.train(viable_combos, board)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(model.history.history['accuracy'], c='k')
    plt.ylabel('training accuracy')
    plt.xlabel('epochs')
    plt.twinx()
    plt.plot(model.history.history['loss'], c='b')
    plt.ylabel('training loss (error)')
    plt.title('training')

    plt.subplot(1, 2, 2)
    plt.plot(model.history.history['val_accuracy'], c='k')
    plt.ylabel('testing accuracy')
    plt.xlabel('epochs')
    plt.twinx()
    plt.plot(model.history.history['val_loss'], c='b')
    plt.ylabel('testing loss (error)')
    plt.title('testing')
    plt.tight_layout()
    plt.show()