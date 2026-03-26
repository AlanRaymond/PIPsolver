from itertools import product
from enum import Enum, auto

from .domain import DomainNode

class Condition(Enum):
    EQUAL_TO = auto(),
    GREATER_THAN = auto(),
    LESSER_THAN = auto(),
    ALL_EQUAL = auto(),
    ALL_NOT_EQUAL = auto()

class Constraint:
    def __init__(self, nodes: tuple[str], target_value: int | None = None, condition: Condition = Condition.EQUAL_TO):
        self._target_value = target_value
        self._condition = condition
        
        self.nodes = nodes
    
    def _satisfies(self, s: tuple[int]) -> bool:
        match self._condition:
            case Condition.EQUAL_TO:
                return sum(s) == self._target_value
            case Condition.GREATER_THAN:
                return sum(s) > self._target_value
            case Condition.LESSER_THAN:
                return sum(s) < self._target_value
            # default, don't filter
            case _:
                return True
    
    def relation(self) -> callable:
        def generate_allowed_sets(nodes: tuple[DomainNode]) -> list[set[int]]:
            if not nodes:
                raise ValueError("No nodes were specified")

            # Build cartesian product of pips domains
            values = [sorted(node.values) for node in nodes]
            all_combinations = product(*values)
            
            # Keep only combinations that satisfy the condition
            valid_combinations = [combination for combination in all_combinations
                                  if self._satisfies(combination)]
            
            # For each tile, build the set of values that are valid
            allowed_sets = [set() for _ in nodes]
            for combination in valid_combinations:
                for index, value in enumerate(combination):
                    allowed_sets[index].add(value)
                    
            return allowed_sets
        return generate_allowed_sets
        
    def __str__(self):
        return f"({self.nodes}, ({self._condition.name} {"" if self._target_value is None else self._target_value}))"

    def __repr__(self):
        return self.__str__()
    
class ConstraintAllEqual(Constraint):
    def __init__(self, nodes, condition, values):
        super().__init__(nodes = nodes, target_value = None, condition = condition)
        self._values = values
    
    def _satisfies(self, s: tuple[int]) -> bool:
        nodes_share_common_value = len(set(s)) == 1
        
        number_of_tiles = len(s)        
        valid_values = [value for value, count in self._values.items()
                        if count >= number_of_tiles]
        number_of_values_matches_tiles = s[0] in set(valid_values)
        
        return nodes_share_common_value and number_of_values_matches_tiles

class ConstraintAllNotEqual(Constraint):
    def __init__(self, nodes, condition):
        super().__init__(nodes = nodes, target_value = None, condition = condition)
    
    def _satisfies(self, s: tuple[int]) -> bool:
        number_of_unique_values = len(set(s))
        number_of_tiles = len(s)
        return number_of_unique_values == number_of_tiles