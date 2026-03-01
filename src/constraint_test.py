import unittest

from constraint import Condition, constraint
from tile import Tile
from domino import Domino
from domain import Domain

class TestConstraintValidation(unittest.TestCase):
    def setUp(self):
        self.tile1 = Tile(id = "A1", neighbours = {"A2"})
        self.tile2 = Tile(id = "B1", neighbours = {"B2"})

    def tearDown(self):
        self.tile1 = None
        self.tile2 = None

    def test_valid_condition(self):
        # passing the class a condition variable that is not
        # a Condition enum
        tiles = [self.tile1]
        target_value = 5
        condition = "greater_than"

        with self.assertRaises(ValueError):
            constraint_invalid_condition = constraint(tiles = tiles,
                                                      target_value = target_value,
                                                      condition = condition)

    def test_no_tiles(self):
        tiles = []
        target_value = 3
        condition = Condition.EQUAL_TO

        with self.assertRaises(ValueError):
            constraint_no_tiles = constraint(
                    tiles = tiles,
                    target_value = target_value,
                    condition = condition)

    def test_constrain_invalid_tile(self):
        tiles = [self.tile1]
        target_value = 3
        condition = Condition.EQUAL_TO

        constraint_tile1 = constraint(tiles = tiles,
                                      target_value = target_value,
                                      condition = condition)

        with self.assertRaises(ValueError):
            constraint_tile1(self.tile2)


class TestConstraintFunction(unittest.TestCase):
    def setUp(self):
        self.tile1 = Tile(id = "A1", neighbours = {"A2", "A3"})
        self.tile2 = Tile(id = "A2", neighbours = {"A1", "A3"})
        self.tile3 = Tile(id = "A3", neighbours = {"A1", "A2"})
        self.tile3.pips = Domain({3,4})

    def tearDown(self):
        self.tile1 = None
        self.tile2 = None
        self.tile3 = None

    def test_equal_to(self):
        tiles = [self.tile1, self.tile2]
        target_value = 4
        condition = Condition.EQUAL_TO

        tile = tiles[0]

        constraint_equal_to = constraint(tiles = tiles,
                                         target_value = target_value,
                                         condition = condition)
        constraint_equal_to(tile)
        
        expected_value = {0, 1, 2, 3, 4}

        self.assertEqual(tile.pips.values, expected_value)

    def test_greater_than(self):
        tiles = [self.tile1, self.tile2]
        target_value = 11
        condition = Condition.GREATER_THAN

        tile = tiles[0]

        constraint_greater_than = constraint(tiles = tiles,
                                             target_value = target_value,
                                             condition = condition)
        constraint_greater_than(tile)

        expected_value = {6}

        self.assertEqual(tile.pips.values, expected_value)

    def test_lesser_than(self):
        tiles = [self.tile1, self.tile2]
        target_value = 5
        condition = Condition.LESSER_THAN

        tile = tiles[0]

        constraint_lesser_than = constraint(tiles = tiles,
                                            target_value = target_value,
                                            condition = condition)
        constraint_lesser_than(tile)

        expected_value = {0, 1, 2, 3, 4}

        self.assertEqual(tile.pips.values, expected_value)

    def test_all_equal(self):
        tiles = [self.tile1, self.tile3]
        condition = Condition.ALL_EQUAL

        tile = tiles[0]

        constraint_all_equal = constraint(tiles = tiles,
                                          condition = condition)
        constraint_all_equal(tile)

        expected_value = {3, 4}

        self.assertEqual(tile.pips.values, expected_value)

    def test_all_not_equal(self):
        self.tile3.pips = Domain({3})

        tiles = [self.tile1, self.tile3]
        condition = Condition.ALL_NOT_EQUAL

        tile = tiles[0]

        constraint_all_not_equal = constraint(tiles = tiles,
                                              condition = condition)
        constraint_all_not_equal(tile)

        expected_value = {0, 1, 2, 4, 5, 6}

        self.assertEqual(tile.pips.values, expected_value)


if __name__ == "__main__":
    unittest.main()
