import unittest

from tile import Tile
from domino import Domino

class TestTileAttributes(unittest.TestCase):
    test_id = "B1"
    test_neighbours = {"A1", "A2", "B2"}
    test_dominoes = {
            Domino(1, 2),
            Domino(2, 3)
            }

    def test_instantiation(self):
        self.assertIsInstance(
                Tile(
                    id = self.test_id,
                    neighbours = self.test_neighbours,
                    dominoes = self.test_dominoes
                    ),
                Tile
                )

    def test_values_generation(self):
        test_tile = Tile(id = self.test_id,
                         neighbours = self.test_neighbours,
                         dominoes = self.test_dominoes)

        expected_output = {1, 2, 3}

        self.assertEqual(test_tile.values, expected_output)

class TestTileIsSingleton(unittest.TestCase):
    
    tile_a = Tile(id = "A",
                  neighbours = {"B"},
                  dominoes = {Domino(1, 2), Domino(3, 4)})
    tile_b = Tile(id = "B",
                  neighbours = {"A"},
                  dominoes = {Domino(1, 2)})
    tile_c = Tile(id = "C",
                  neighbours = {"D"},
                  dominoes = {Domino(1, 2)})
    tile_c.values = {1,}

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.tile_a.is_singleton('invalid')

    def test_neighbours_singleton(self):
        self.assertTrue(self.tile_a.is_singleton('neighbours'))

    def test_dominoes_singleton(self):
        self.assertTrue(self.tile_b.is_singleton('dominoes'))

    def test_values_not_singleton(self):
        self.assertFalse(self.tile_b.is_singleton('values'))

    def test_values_singleton(self):        
        self.assertTrue(self.tile_c.is_singleton('values'))

    def test_all_not_singleton(self):
        self.assertFalse(self.tile_a.is_singleton('all'))

    def test_all_singleton(self):
        self.assertTrue(self.tile_c.is_singleton('all'))


if __name__ == "__main__":
    unittest.main()
