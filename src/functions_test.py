import unittest

from functions import Condition, constraint, update_dominoes, update_pips, exclude_neighbour, exclude_domino, restrict_dominoes, pair_tile
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
        invalid_condition = "greater_than"

        with self.assertRaises(ValueError):
            constraint(tiles = tiles, target_value = target_value,
                       condition = invalid_condition)

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

class TestUpdateFunctions(unittest.TestCase):
    def setUp(self):
        self.tile1 = Tile(id = "A1", neighbours = {"A2"})
        self.tile1.pips = Domain({0})
                
        self.tile2 = Tile(id = "B1", neighbours = {"B2"})
        self.tile2.dominoes = Domain({Domino(0, 0), Domino(0, 1), Domino(1, 5)})

    def tearDown(self):
        self.tile1 = None
        self.tile2 = None
    
    def test_update_dominoes(self):
        update_dominoes(self.tile1)
        expected_dominoes = {Domino(0, 0), Domino(0, 1), Domino(0, 2),
                             Domino(0, 3), Domino(0, 4), Domino(0, 5),
                             Domino(0, 6)}
        
        self.assertEqual(self.tile1.dominoes.values, expected_dominoes)
        
    def test_update_pips(self):
        update_pips(self.tile2)
        expected_pips = {0, 1, 5}
        
        self.assertEqual(self.tile2.pips.values, expected_pips)

class TestJobFunctions(unittest.TestCase):
    def setUp(self):
        self.tile1 = Tile(id = "A1", neighbours = {"A2", "A3"})
        self.tile1.pips = Domain({0, 1, 2, 3, 4, 5, 6})
        self.tile1.dominoes = Domain({Domino(0, 0), Domino(0, 1), Domino(1, 5)})

    def tearDown(self):
        self.tile1 = None
    
    def test_exclude_domino(self):
        exclude_domino(Domino(0, 1))(self.tile1)
        expected_dominoes = {Domino(0, 0), Domino(1, 5)}
        
        self.assertEqual(self.tile1.dominoes.values, expected_dominoes)
    
    def test_exclude_neighbour(self):
        exclude_neighbour("A2")(self.tile1)
        expected_neighbours = {"A3"}
        
        self.assertEqual(self.tile1.neighbours.values, expected_neighbours)
    
    def test_restrict_dominoes(self):
        allowed_dominoes = {Domino(0, 0), Domino(1, 5)}
        restrict_dominoes(allowed_dominoes)(self.tile1)
        
        expected_dominoes = allowed_dominoes
        
        self.assertEqual(self.tile1.dominoes.values, expected_dominoes)
    
    def test_pair_tile(self):
        tile2 = Tile(id = "A2", neighbours = {"A1", "A3"})
        pair_tile(self.tile1)(tile2)
        
        expected_neighbours = {"A1"}
        
        self.assertEqual(tile2.neighbours.values, expected_neighbours)


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
        
        expected_pips = {0, 1, 2, 3, 4}
        expected_dominoes = {Domino(0, 0), Domino(0, 1), Domino(0, 2),
                             Domino(0, 3), Domino(0, 4), Domino(0, 5),
                             Domino(0, 6),
                             Domino(1, 1), Domino(1, 2), Domino(1, 3),
                             Domino(1, 4), Domino(1, 5), Domino(1, 6),
                             Domino(2, 2), Domino(2, 3), Domino(2, 4),
                             Domino(2, 5), Domino(2, 6),
                             Domino(3, 3), Domino(3, 4), Domino(3, 5),
                             Domino(3, 6),
                             Domino(4, 4), Domino(4, 5), Domino(4, 6)}

        self.assertEqual(tile.pips.values, expected_pips)
        self.assertEqual(tile.dominoes.values, expected_dominoes)

    def test_greater_than(self):
        tiles = [self.tile1, self.tile2]
        target_value = 11
        condition = Condition.GREATER_THAN

        tile = tiles[0]

        constraint_greater_than = constraint(tiles = tiles,
                                             target_value = target_value,
                                             condition = condition)
        constraint_greater_than(tile)

        expected_pips = {6}
        expected_dominoes = {Domino(0, 6), Domino(1, 6), Domino(2, 6),
                             Domino(3, 6), Domino(4, 6), Domino(5, 6),
                             Domino(6, 6)}

        self.assertEqual(tile.pips.values, expected_pips)
        self.assertEqual(tile.dominoes.values, expected_dominoes)

    def test_lesser_than(self):
        tiles = [self.tile1, self.tile2]
        target_value = 2
        condition = Condition.LESSER_THAN

        tile = tiles[0]

        constraint_lesser_than = constraint(tiles = tiles,
                                            target_value = target_value,
                                            condition = condition)
        constraint_lesser_than(tile)

        expected_pips = {0, 1}
        expected_dominoes = {Domino(0, 0), Domino(0, 1), 
                             Domino(1, 1),
                             Domino(2, 0), Domino(2, 1),
                             Domino(3, 0), Domino(3, 1),
                             Domino(4, 0), Domino(4, 1),
                             Domino(5, 0), Domino(5, 1),
                             Domino(6, 0), Domino(6, 1)}

        self.assertEqual(tile.pips.values, expected_pips)
        self.assertEqual(tile.dominoes.values, expected_dominoes)

    def test_all_equal(self):
        tiles = [self.tile1, self.tile3]
        condition = Condition.ALL_EQUAL

        tile = tiles[0]

        constraint_all_equal = constraint(tiles = tiles,
                                          condition = condition)
        constraint_all_equal(tile)

        expected_pips = {3, 4}
        expected_dominoes = {Domino(0, 3), Domino(0, 4),
                             Domino(1, 3), Domino(1, 4),
                             Domino(2, 3), Domino(2, 4),
                             Domino(3, 3), Domino(3, 4),
                             Domino(4, 4),
                             Domino(5, 3), Domino(5, 4),
                             Domino(6, 3), Domino(6, 4)}

        self.assertEqual(tile.pips.values, expected_pips)
        self.assertEqual(tile.dominoes.values, expected_dominoes)

    def test_all_not_equal(self):
        self.tile3.pips = Domain({3})

        tiles = [self.tile1, self.tile3]
        condition = Condition.ALL_NOT_EQUAL

        tile = tiles[0]

        constraint_all_not_equal = constraint(tiles = tiles,
                                              condition = condition)
        constraint_all_not_equal(tile)

        expected_pips = {0, 1, 2, 4, 5, 6}
        expected_dominoes = {Domino(0, 0), Domino(0, 1), Domino(0, 2),
                             Domino(0, 3), Domino(0, 4), Domino(0, 5),
                             Domino(0, 6),
                             Domino(1, 1), Domino(1, 2), Domino(1, 3),
                             Domino(1, 4), Domino(1, 5), Domino(1, 6),
                             Domino(2, 2), Domino(2, 3), Domino(2, 4),
                             Domino(2, 5), Domino(2, 6),
                             Domino(3, 4), Domino(3, 5), Domino(3, 6),
                             Domino(4, 4), Domino(4, 5), Domino(4, 6),
                             Domino(5, 5), Domino(5, 6),
                             Domino(6, 6)} # No Domino(3, 3)

        self.assertEqual(tile.pips.values, expected_pips)
        self.assertEqual(tile.dominoes.values, expected_dominoes)


if __name__ == "__main__":
    unittest.main()
