import unittest

from domain import Domain

class TestDomainAttributes(unittest.TestCase):
    values_same_type = {"A1", "B2", "A1"}
    values_not_same_type = {"A1", 4}

    def test_instance_same_type(self):
        self.assertIsInstance(
                Domain(self.values_same_type),
                Domain)

    def test_instance_not_same_type(self):
        with self.assertRaises(TypeError):
            Domain(self.values_not_same_type)

    def test_set_values(self):
        domain = Domain()
        domain.values = self.values_same_type

        self.assertEqual(domain.values, set(self.values_same_type))

    def test_set_values_invalid(self):
        domain = Domain()
        with self.assertRaises(TypeError):
            domain.values = self.values_not_same_type


if __name__ == "__main__":
    unittest.main()
