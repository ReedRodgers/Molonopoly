from unittest import TestCase
from InputGenerator import Board, Player, Property, find_all_combos, generate_training_input
from collections import Counter

p_expensive = Property(105, 'blue')
p1 = Property(100, 'yellow')
p3 = Property(100, 'red')
p2 = Property(100, 'blue')
p_cheap = Property(99, 'red')
p_free = Property(1, 'green')
poor_player = Player(99)
rich_player = Player(100000)
modest_player = Player(299)


class TestFindAllCombos(TestCase):
    def test_single_property(self):
        """Single property should return a single property combination"""
        prop = [Property(100, 'blue')]
        board = Board(prop)
        combos = find_all_combos(board)
        self.assertSetEqual({frozenset(), frozenset(prop)}, combos)

    def test_triple_property(self):
        """Tests higher order combinations of properties"""
        properties = [p1, p2, p3]
        board = Board(properties)
        combos = find_all_combos(board)
        manual_combos = {frozenset([]), frozenset([p1]), frozenset([p2]), frozenset([p3]),
                         frozenset([p1, p2]),
                         frozenset([p1, p3]),
                         frozenset([p2, p3]),
                         frozenset([p1, p2, p3])}
        self.assertSetEqual(combos, manual_combos)


class TestTrainingInput(TestCase):

    def test_non_negative_cash(self):
        """should return empty set if cash too low"""
        combos = {frozenset([p_cheap, p1]), frozenset([p_cheap, p_free]), frozenset([p1])}
        viable_combos = generate_training_input(combos, poor_player.cash)
        self.assertListEqual([], viable_combos)

    def test_too_much_money(self):
        """when cash exceeds value of all properties, property sets should be the same as those produced by find_all_combos"""
        """final cash should be initial - sum property value"""
        combo = frozenset([p_cheap, p1, p2, p3, p_expensive, p_free])
        combos = {combo}
        viable_combos = generate_training_input(combos, rich_player.cash)
        resultant_cash = rich_player.cash - sum([prop.cost for prop in combo])
        self.assertListEqual([{'cash': resultant_cash, 'properties': combo}], viable_combos)

    def test_multiple_sets(self):
        """no viable property set should be excluded"""
        self.maxDiff = None
        s1 = frozenset([p1, p2])
        s2 = frozenset([p_free, p2])
        s3 = frozenset([p_cheap, p2])
        s4 = frozenset([p_cheap, p1, p2])
        s5 = frozenset([p1, p2, p3])
        combos = {s1, s2, s3, s4, s5}
        viable_combos = generate_training_input(combos, modest_player.cash)

        temp = [(combo['cash'], combo) for combo in viable_combos]
        temp.sort()
        viable_combos = [combo for (key, combo) in temp]

        result = [{'cash': 0, 'properties': s4},
                  {'cash': 99, 'properties': s1},
                  {'cash': 100, 'properties': s3},
                  {'cash': 198, 'properties': s2}]

        self.assertListEqual(viable_combos, result)


class TestBoard(TestCase):
    def test_get_colors(self):
        b1 = Board([p1])  # Single property
        self.assertEqual(Counter({p1.color: 1}), b1.get_colors())
        b2 = Board([p1, p2])  # Multiple properties, single colors
        self.assertEqual(Counter({p1.color: 1, p2.color: 1}), b2.get_colors())
        b3 = Board([p3, p_cheap])  # Single color, multiple properties
        self.assertEqual(Counter({p3.color: 2}), b3.get_colors())
        b4 = Board([p3, p_cheap, p_free, p_expensive])  # Multiple color, multiple properties
        self.assertEqual(Counter({p3.color: 2, p_free.color: 1, p_expensive.color: 1}), b4.get_colors())
