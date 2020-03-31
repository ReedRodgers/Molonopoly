from unittest import TestCase
from InputGenerator import Board, Property
from network import read_board, evaluate_heuristic
import numpy as np

pb1 = Property(100, 'b')
pb2 = Property(100, 'b')
pb3 = Property(100, 'b')

py1 = Property(100, 'y')
py2 = Property(100, 'y')
py3 = Property(100, 'y')

pr1 = Property(100, 'r')
pr2 = Property(100, 'r')
pr3 = Property(100, 'r')

props1 = [pb1, pb2]
props1_1 = [pb1, pr2]
props2 = [pb1]
props3 = [pb1, pb2, py1, pr1]
props4 = [pb1, pb2, pb3,
          py1, py2, py3,
          pr1, pr2, pr3]
props4_1 = [pb1, pb2, py1, py2]

board1 = Board(props1)
board2 = Board(props2)
board3 = Board(props3)
board4 = Board(props4)


class Test(TestCase):
    def test_read_board(self):
        combo1 = {'cash': 100, 'properties': props1}
        combo2 = {'cash': 100, 'properties': props2}
        combo3 = {'cash': 100, 'properties': props3}
        combo4 = {'cash': 100, 'properties': props4}
        combo4_1 = {'cash': 100, 'properties': props4_1}
        output1 = np.array([100, 1, 1])
        output2 = np.array([100, 1])
        output3 = np.array([100, 1, 1, 1, 0, 1, 0])
        output4 = np.array([100,
                            1, 1, 1,
                            1, 1, 1,
                            1, 1, 1])
        output4_1 = np.array([100,
                              1, 1, 0,
                              1, 1, 0,
                              0, 0, 0])
        np.testing.assert_array_equal(output1, read_board([combo1], board1)[0])
        np.testing.assert_array_equal(output2, read_board([combo2], board2)[0])
        np.testing.assert_array_equal(output3, read_board([combo3], board3)[0])

        for output, expected in zip(read_board([combo4, combo4_1], board4), [output4, output4_1]):
            np.testing.assert_array_equal(output, expected)


    def test_evaluate_heuristic(self):
        """Value of a two properties is twice the value of one property, given no cash"""
        combo1 = {'cash': 0, 'properties': [pb1]}
        combo2 = {'cash': 0, 'properties': [pb1, pb2]}
        combo3 = {'cash': 0, 'properties': [pb1, pr2]}
        self.assertEqual(evaluate_heuristic(combo1, board4) * 2, evaluate_heuristic(combo2, board4))
        self.assertEqual(evaluate_heuristic(combo3, board4), evaluate_heuristic(combo2, board4))
        """Value of a triad is greater than twice the value of two properties (Assuming three total properties)""" # 2 * modifyer is arbitrary
        combo4 = {'cash': 0, 'properties': [pb1, pb2, pb3]}
        self.assertGreaterEqual(evaluate_heuristic(combo4, board4), evaluate_heuristic(combo2, board4))
        """Value of triad of same color > than that of differing colors"""
        combo5 = {'cash': 0, 'properties': [pb1, pb2, pr3]}
        self.assertGreater(evaluate_heuristic(combo4, board4), evaluate_heuristic(combo5, board4))
        """Value of cash is based loosely on the value of the property combinations that could be acquired with said cash, and their likelihood"""
        # As per the statement above, cash value should be null when:
            #all properties are owned
        combo6 = {'cash': 0, 'properties': props3}
        combo6_1 = {'cash': 100, 'properties': props3}
        self.assertEqual(evaluate_heuristic(combo6, board3), evaluate_heuristic(combo6_1, board3))
            # the cash is not enough to purchase more properties
        combo6_2 = {'cash': 10, 'properties': props3}
        self.assertEqual(evaluate_heuristic(combo6, board4), evaluate_heuristic(combo6_2, board4))
            # the cash is more than enough to purchase more properties
        combo6_4 = {'cash': 20000, 'properties': props3}
        combo6_5 = {'cash': 10000, 'properties': props3}
        self.assertEqual(evaluate_heuristic(combo6_4, board4), evaluate_heuristic(combo6_5, board4))
        # The same amount of cash should be more valuable when the remaining property will complete a set than when it would not
        combo6_6 = {'cash': 100, 'properties': props1_1}
        combo6_7 = {'cash': 100, 'properties': props1}
        self.assertGreater(evaluate_heuristic(combo6_7, board4), evaluate_heuristic(combo6_6, board4))
