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
    def values(self, values) -> set:
        datatypes = {type(value) for value in values}

        all_same_type = len(datatypes) == 1

        if not all_same_type:
            raise TypeError("All items in the domain need to be the same type")

        self._values = set(values)

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
    def check_for_invalid_collapse(self) -> bool:
        if self.is_empty:
            raise ValueError("Domain collapsed to empty after removal.")
        return True

    # ==========================================
    # METHODS
    # ==========================================

    def intersects(self, other: set) -> bool:
        return bool(self._values & other)

    def remove(self, value) -> bool:
        """Remove a single value from the domain. Useful to constrain neighbours"""
        if value not in self._values:
            return False
        
        before = self.size
        self._values.remove(value)
        self.check_for_invalid_collapse()
        changed = self.size != before
        return changed

    def restrict_to(self, allowed) -> bool:
        """ Uses set operations to restrict the domain. Useful for dominoes or pips sets."""
        allowed_set = set(allowed)

        before = self.size
        self._values.intersection_update(allowed_set)
        self.check_for_invalid_collapse()
        changed = self.size != before
        return changed

    def copy(self) -> "Domain":
        return Domain(self._values)

    # ==========================================
    # OPERATIONS
    # ==========================================
    def __iter__(self):
        """Enables less verbose iteration."""
        try:
            sorted_values = sorted(self._values)
        except TypeError: # if values cannot be sorted
            sorted_values = list(self.values)
        yield from sorted_values

