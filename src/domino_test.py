import unittest
from unittest.mock import patch
from io import StringIO

from domino import Domino

class TestCreation(unittest.TestCase):

    def test_instantiation(self):
        self.assertIsInstance(Domino(2, 1), Domino)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            Domino(7, 1)

    def test_print_unequal(self):
        input = (2, 1)
        expected_output = "[1, 2]\n"

        with patch('sys.stdout', new = StringIO()) as console:
            print(Domino(*input))
            self.assertEqual(console.getvalue(), expected_output)

    def test_print_equal(self):
        input = (3, 3)
        expected_output = "[3, 3]\n"

        with patch('sys.stdout', new = StringIO()) as console:
            print(Domino(*input))
            self.assertEqual(console.getvalue(), expected_output)

    def test_not_equal(self):
        a, b, c, d = 1, 2, 3, 4
        
        self.assertFalse(Domino(a, b) == Domino(c, d))

    def test_equal(self):
        a, b, c, d = 3, 4, 4, 3

        self.assertTrue(Domino(a, b) == Domino(c, d))

    def test_unable_to_compare(self):
        a, b = 1, 2

        with self.assertRaises(NotImplementedError):
            Domino(a, b) == 5

    def test_hashable(self):
        dominoes = set()
        dominoes.add( Domino(1, 2) )

        domino = Domino(1, 2)

        self.assertTrue(domino in dominoes)

if __name__ == "__main__":
    unittest.main()
