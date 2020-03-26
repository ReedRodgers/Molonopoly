from unittest import TestCase
from InputGenerator import Board, Property
from network import read_board

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
props2 = [pb1]
props3 = [pb1, pb2, py1, pr1]
props4 = [pb1, pb2, pb3, py1, py2, py3, pr1, pr2, pr3]
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
        output1 = [100, 1, 1]
        output2 = [100, 1]
        output3 = [100, 1, 1, 1, 0, 1, 0]
        output4 = [100,
                   1, 1, 1,
                   1, 1, 1,
                   1, 1, 1]
        output4_1 = [100,
                     1, 1, 0,
                     1, 1, 0,
                     0, 0, 0]
        self.assertEqual([output1], read_board([combo1], board1))
        self.assertEqual([output2], read_board([combo2], board2))
        self.assertEqual([output3], read_board([combo3], board3))
        self.assertEqual([output4, output4_1], read_board([combo4, combo4_1], board4))
