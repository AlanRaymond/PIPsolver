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
    def __init__(self, 
                 nodes: tuple[str],
                 target_value: int | None = None,
                 condition: Condition = Condition.ALL_EQUAL):
        self._target_value = target_value
        self._condition = condition        
        
        self.nodes = nodes
        self.relation = relation(target_value, condition)
    
    def __str__(self):
        return f"({self.nodes}, ({self._condition.name} {"" if self._target_value is None else self._target_value}))"

    def __repr__(self):
        return self.__str__()

def relation(target_value: int | None = None,
               condition: Condition = Condition.ALL_EQUAL
               ) -> callable:
    
    if not isinstance(condition, Condition):
        raise ValueError("Invalid condition")
    
    # ------------------------------------------
    # FILTER FUNCTION
    # ------------------------------------------

    def _satisfies(s: tuple[int], target_value, condition) -> bool:
        '''A helper function to return a filter to yield only valid pips when a constraint is applied'''
        number_of_tiles = len(s)
        number_of_unique_values = len(set(s))

        target_value_not_specified = target_value is None
        constraint_requires_value = condition not in {Condition.ALL_EQUAL, Condition.ALL_NOT_EQUAL}

        if target_value_not_specified and constraint_requires_value:
            raise ValueError(f"Specify a target value. Currently: {target_value}")
        
        match condition:
            case Condition.EQUAL_TO:
                return sum(s) == target_value
            case Condition.GREATER_THAN:
                return sum(s) > target_value
            case Condition.LESSER_THAN:
                return sum(s) < target_value
            case Condition.ALL_EQUAL:
                return number_of_unique_values == 1
            case Condition.ALL_NOT_EQUAL:
                return number_of_unique_values == number_of_tiles
            # default, don't filter
            case _:
                return True
    
    def generate_allowed_sets(nodes: tuple[DomainNode]) -> list[set[int]]:
        if not nodes:
            raise ValueError("No nodes were specified")
        
        # Build cartesian product of pips domains

        values = [sorted(node.values) for node in nodes]
        all_combinations = product(*values)

        # Keep only combinations that satisfy the condition
    
        valid_combinations = [combination 
                          for combination in all_combinations 
                          if _satisfies(s=combination, target_value=target_value, condition=condition)
                          ]

        # For each tile, build the set of values that are valid

        allowed_sets = [set() for node in nodes]
        for combination in valid_combinations:
            for index, value in enumerate(combination):
                allowed_sets[index].add(value)
        
        return allowed_sets
    return generate_allowed_sets

