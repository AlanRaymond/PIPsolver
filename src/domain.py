class Domain:
    """
    A domain represents a set of possible values in a sample space.
    It supports mutations, entropy, and collapse checks.
    """
    def __init__(self, values: set = set()):
        datatypes = {type(value) for value in values}
        not_all_same_type = len(datatypes) > 1
        if not_all_same_type:
            raise TypeError("All items in the domain need to be the same type")

        self._values = values

    @property
    def values(self) -> set:
        return self._values

    @values.setter
    def values(self, values) -> bool:
        datatypes = {type(value) for value in values}

        all_same_type = len(datatypes) == 1

        if not all_same_type:
            raise TypeError("All items in the domain need to be the same type")

        self._values = set(values)
        
        return True

    @property
    def size(self) -> int:
        return len(self._values)

    @property
    def is_empty(self) -> bool:
        return self.size == 0

    @property
    def is_singleton(self) -> bool:
        return self.size == 1

    @property
    def datatype(self):
        if self.size == 0:
            return None
        sample_element = list(self._values)[0]
        return type(sample_element)

    # ==========================================
    # METHODS
    # ==========================================

    def intersects(self, other: set) -> bool:
        return bool(self._values & other)


    def remove(self, value) -> bool:
        """Remove a single value from the domain. Useful to constrain neighbours.
        Only mutates if the domain doesn't collapse to a null set after the operation. Returns True if changed."""
        if type(value) != self.datatype:
            return False

        if value not in self._values:
            return False

        collapse_to_null = (self.size == 1) and (value in self._values)
        if collapse_to_null:
            return False

        new_values = self._values.copy()
        new_values.remove(value)
        
        self._values = new_values        

        return True


    def restrict_to(self, allowed: set) -> bool:
        """
        Uses set operations to restrict the domain. Useful for dominoes or pips sets.
        Only mutates if the domain doesn't collapse to a null set after the operation.
        Returns True if changed.
        """
        new_values = self._values.copy() & allowed
        
        if new_values == set():
            return False

        self._values = new_values
        return True


    def copy(self) -> "Domain":
        return Domain(self._values)

    # ==========================================
    # OPERATIONS
    # ==========================================
    def __contains__(self, item):
        return item in self._values

    def __iter__(self):
        """Enables less verbose iteration."""
        try:
            sorted_values = sorted(self._values)
        except TypeError: # if values cannot be sorted
            sorted_values = list(self.values)
        yield from sorted_values

    def __repr__(self):
        return f"Domain(Type: {self.datatype}, Count: {self.size})"