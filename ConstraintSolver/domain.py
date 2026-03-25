from .domino import Domino

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
        if self.is_empty:
            return None
        sample_element = list(self._values)[0]
        return type(sample_element)

    # ==========================================
    # METHODS
    # ==========================================
    def remove(self, value) -> bool:
        """
        Remove a single value from the domain.
        Returns True if changed.
        """
        if type(value) != self.datatype:
            # do nothing
            return False

        if value not in self._values:
            # do nothing
            return False

        collapse_to_null = (self.size == 1) and (value in self._values)
        if collapse_to_null:
            raise ValueError(f"Domain collapsed to a null set.")

        new_values = self._values.copy()
        new_values.remove(value)
        
        self._values = new_values        

        return True


    def restrict_to(self, allowed: set) -> bool:
        """
        Uses set operations to restrict the domain.
        Returns True if changed.
        """
        original_values = self._values.copy()
        new_values = original_values & allowed
        
        has_changed = new_values != original_values
        
        if has_changed:
            self._values = new_values
        
        return has_changed


    def copy(self) -> "Domain":
        return Domain(self._values)

    # ==========================================
    # OPERATIONS
    # ==========================================
    def __contains__(self, item):
        return item in self._values
    
    def _sorted_values(self):
        try:
            return sorted(self._values)
        except TypeError: # if values cannot be sorted
            return list(self._values)

    def __iter__(self):
        """Enables less verbose iteration."""
        yield from self._sorted_values()
        
    def __str__(self):
        return f"{self._sorted_values()}"

class DomainNode(Domain): # Tile
    """
    A domain that represents the possible values for a node. This is a set of integers.
    It supports the same operations as a normal domain, but with interaction with Edge domains.
    """
    def __init__(self, values: set = set(range(7))):
        super().__init__(values)

        if self.datatype is not None and self.datatype != int:
            raise TypeError("All items in the domain need to be of type int")
    
class DomainEdge(Domain): # Domino
    """
    A domain that represents the possible values for an edge between two tiles.
    This is a set of dominoes. It supports the same operations as a normal domain, 
     but with interaction between with Node domains.
    """
    def __init__(self, node_a: str, node_b: str, values: set = set()):
        self.node_a = node_a
        self.node_b = node_b
        super().__init__(values)

        if self.datatype is not None and self.datatype != Domino:
            raise TypeError("All items in the domain need to be of type Domino")
        
    ### NOT CURRENTLY USED
    # get functions used to restrict node domains.
    @property
    def values_a(self) -> set:
        return {domino.values[0] for domino in self._values}
    @property
    def values_b(self) -> set:
        return {domino.values[1] for domino in self._values}
        
        # set functions used to restrict self.values.
    def update_values(self, node: str, values: set) -> bool:
        if self.datatype is not None and self.datatype != Domino:
            raise TypeError("All items in the domain need to be of type Domino")
        if node not in (self.node_a, self.node_b):
            raise ValueError("Node not in edge")
            
        position = 0 if node == self.node_a else 1
            
        restricted_dominoes = {domino for domino in self._values
                               if domino.values[position] in values}
            
        return self.restrict_to(restricted_dominoes)
