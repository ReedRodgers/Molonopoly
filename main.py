from InputGenerator import Property, Player, Board, find_all_combos, generate_training_input
import network
import matplotlib.pyplot as plt

if __name__ == '__main__':
    prop_val = 100
    pb1 = Property(prop_val, 'b')
    pb2 = Property(prop_val, 'b')
    pb3 = Property(prop_val, 'b')

    py1 = Property(prop_val, 'y')
    py2 = Property(prop_val, 'y')
    py3 = Property(prop_val, 'y')

    pr1 = Property(prop_val, 'r')
    pr2 = Property(prop_val, 'r')
    pr3 = Property(prop_val, 'r')

    pg1 = Property(prop_val, 'g')
    pg2 = Property(prop_val, 'g')
    pg3 = Property(prop_val, 'g')


    pp1 = Property(200, 'p')
    pp2 = Property(200, 'p')

    pc1 = Property(50, 'c')
    pc2 = Property(50, 'c')


    props = [pb1, pb2, pb3,
             py1, py2, py3,
             pr1, pr2, pr3,
             pg1, pg2, pg3,
             pp1, pp2, pc1, pc2]

    board = Board(props)
    player1 = Player(500)
    all_combos = find_all_combos(board)
    viable_combos = generate_training_input(all_combos, player1.cash)
    model = network.train(viable_combos, board)

    plt.figure(figsize=(12, 5))
    plt.subplot(2, 2, 1)
    plt.plot(model.history.history['accuracy'], c='k')
    plt.ylabel('training accuracy')
    plt.xlabel('epochs')
    plt.subplot(2, 2, 2)
    plt.plot(model.history.history['loss'], c='b')
    plt.ylabel('training loss (error)')
    plt.title('training')

    plt.subplot(2, 2, 3)
    plt.plot(model.history.history['val_accuracy'], c='k')
    plt.ylabel('testing accuracy')
    plt.xlabel('epochs')
    plt.subplot(2, 2, 4)
    plt.plot(model.history.history['val_loss'], c='b')
    plt.ylabel('testing loss (error)')
    plt.title('testing')
    plt.tight_layout()
    plt.show()