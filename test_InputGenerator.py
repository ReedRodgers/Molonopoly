from unittest import TestCase
from InputGenerator import Board, Player, Property, find_all_combos, generate_training_input

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
        self.assertSetEqual(set([frozenset(), frozenset(prop)]), combos)

    def test_triple_property(self):
        """Tests higher order combinations of properties"""
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

    def test_non_negative_cash(self):
        """should return empty property list if cash too low"""
        combos = set(frozenset([p_cheap, p1]), frozenset([p_cheap, p_free]), frozenset([p1]))
        viable_combos = generate_training_input(combos, poor_player)
        self.assertListEqual([{'cash': poor_player.cash, 'properties': []}], viable_combos)

    def test_too_much_money(self):
        """when cash exceeds value of all properties, property sets should be the same as those produced by find_all_combos"""
        """final cash should be initial - sum property value"""
        combo = frozenset([p_cheap, p1, p2, p3, p_expensive, p_free])
        combos = set(combo)
        viable_combos = generate_training_input(combos, rich_player)
        resultant_cash = rich_player.cash = sum([prop.cost for prop in combo])
        self.assertListEqual([{'cash': resultant_cash, 'properties': list(combo)}], viable_combos)

    def test_multiple_sets(self):
        """no viable property set should be excluded"""
        s1 = frozenset([p1, p2])
        s2 = frozenset([p_free, p2])
        s3 = frozenset([p_cheap, p2])
        s4 = frozenset([p_cheap, p1, p2])
        s5 = frozenset([p1, p2, p3])
        sets = [s1, s2, s3, s4, s5]
        combos = set(sets)
        viable_combos = generate_training_input(combos)
        result = [{'cash': 99, 'properties': list(s1),
                   'cash': 198, 'properties': list(s2),
                   'cash': 100, 'properties': list(s3),
                   'cash': 0, 'properties': list(s4)}]
        self.assertListEqual(viable_combos, result)
