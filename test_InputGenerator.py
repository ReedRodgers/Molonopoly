from unittest import TestCase
from InputGenerator import Board, Player, Property, find_all_combos


class TestFindAllCombos(TestCase):
    def test_single_property(self):
        """Single property should return a single property combination"""
        prop = [Property(100, 'blue')]
        board = Board(prop)
        combos = find_all_combos(board)
        self.assertSetEqual(set([frozenset(prop)]), combos)

    def test_triple_property(self):
        """Tests higher order combinations of properties"""
        p1 = Property(100, 'green')
        p3 = Property(100, 'red')
        p2 = Property(100, 'blue')
        properties = [p1, p2, p3]
        board = Board(properties)
        combos = find_all_combos(board)
        manual_combos = set([frozenset([]), frozenset([p1]), frozenset([p2]), frozenset([p3]),
                            frozenset([p1, p2]),
                            frozenset([p1, p3]),
                            frozenset([p2, p3]),
                            frozenset([p1, p2, p3])])
        self.assertSetEqual(combos, manual_combos)


class TestTrainingInput(TestCase):
    def test_generate_training_input(self):

        self.fail()
