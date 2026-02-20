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

    def test_constructor(self):
        domain = Domain(self.values_same_type)

        self.assertEqual(domain.values, set(self.values_same_type))

    def test_set_values(self):
        domain = Domain()
        domain.values = self.values_same_type

        self.assertEqual(domain.values, set(self.values_same_type))

    def test_set_values_invalid(self):
        domain = Domain()
        with self.assertRaises(TypeError):
            domain.values = self.values_not_same_type

class TestDomainProperties(unittest.TestCase):
    empty_domain = Domain()
    filled_domain = Domain({"A", "B", "C"})
    single_domain = Domain({"A"})

    def test_size(self):
        self.assertTrue(self.empty_domain.size == 0)
        self.assertTrue(self.filled_domain.size == 3)
        self.assertTrue(self.single_domain.size == 1)

    def test_is_empty(self):
        self.assertIs(self.empty_domain.is_empty, True)
    
    def test_is_not_empty(self):
        self.assertIs(self.filled_domain.is_empty, False)

    def test_is_singleton(self):
        self.assertIs(self.single_domain.is_singleton, True)

    def test_is_not_singleton(self):
        self.assertIs(self.filled_domain.is_singleton, False)
    
    def test_datatype(self):
        self.assertIs(self.filled_domain.datatype, str)

class TestDomainMethods(unittest.TestCase):
    values_neighbours1 = {"A1", "A2", "B1", "B2"}
    values_neighbours2 = {"A1", "C1"}
    values_neighbours3 = {"D2"}

    def test_copy(self):
        values = {"A1", "B1"}

        domain = Domain(values)
        domain_copy = domain.copy()
        
        self.assertIsNot(domain, domain_copy)

    def test_intersects(self):
        values_a = {"A1", "A2", "B1", "B2"}
        values_b = {"A1", "C1"}
        values_c = {"D2"}

        domain = Domain(values_a)
        self.assertIs(domain.intersects(values_b), True)
        self.assertIs(domain.intersects(values_c), False)

    def test_remove_successful(self):
        original = {"A1", "A2", "B1", "B2"}
        removed = "A1"
        expected = {"A2", "B1", "B2"}

        domain = Domain(original)

        self.assertIs(domain.remove(removed), True)
        self.assertEqual(domain.values, expected)

    def test_remove_unsuccessful(self):
        original = {"A1", "A2", "B1", "B2"}
        removed = "D2"
        expected = original

        domain = Domain(original)
        
        self.assertIs(domain.remove(removed), False)
        self.assertEqual(domain.values, expected)

class TestDomainDunderMethods(unittest.TestCase):
    def test_membership(self):
        member = "A1"
        non_member = "D1"
        collection = {"A1", "A2", "A3"}

        domain = Domain(collection)

        self.assertIs(member in domain, True)
        self.assertIs(non_member in domain, False)

    def test_iteration(self):
        values = {"A1", "A2", "B1", "B2"}
        domain = Domain(values)
        expected = ["A1", "A2", "B1", "B2"]

        self.assertEqual([item for item in domain], expected)


if __name__ == "__main__":
    unittest.main()
