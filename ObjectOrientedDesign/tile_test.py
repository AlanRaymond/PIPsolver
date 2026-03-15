import unittest

from tile import Tile
from domino import Domino
from domain import Domain

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

        expected_output = Domain({1, 2, 3}).values

        self.assertEqual(test_tile.pips.values, expected_output)

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
    tile_c.pips = Domain({1,})

    def test_neighbours_singleton(self):
        self.assertIs(self.tile_a.neighbours.is_singleton, True)

    def test_dominoes_singleton(self):
        self.assertIs(self.tile_b.dominoes.is_singleton, True)

    def test_values_not_singleton(self):
        self.assertIs(self.tile_b.pips.is_singleton, False)

    def test_values_singleton(self):        
        self.assertIs(self.tile_c.pips.is_singleton, True)

    def test_all_not_singleton(self):
        self.assertIs(self.tile_a.is_singleton, False)

    def test_all_singleton(self):
        self.assertIs(self.tile_c.is_singleton, True)


if __name__ == "__main__":
    unittest.main()
