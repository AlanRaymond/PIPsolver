from itertools import product
from enum import Enum, auto
from tile import Tile
from domino import Domino

class Condition(Enum):
    EQUAL_TO = auto(),
    GREATER_THAN = auto(),
    LESSER_THAN = auto(),
    ALL_EQUAL = auto(),
    ALL_NOT_EQUAL = auto()

def update_pips(tile: Tile) -> bool:
    # TODO: Write unit tests for this function
    dominoes_values = set()
    for domino in tile.dominoes.values:
        dominoes_values.update(domino.values)
    intersection = tile.pips.values.intersection(dominoes_values)
    if intersection != tile.pips.values:
        return tile.pips.restrict_to(intersection)
    return False

def update_dominoes(tile: Tile) -> bool:
    # TODO: Write unit tests for this function
    for domino in tile.dominoes.values:
        if not domino.values.issubset(tile.pips.values):
            return tile.dominoes.remove(domino)
    return False

def constraint(tiles: list[Tile],
               target_value: int | None = None,
               condition: Condition = Condition.ALL_EQUAL
               ):
    '''
    Function used to construct a constraint for a tile's pips domain.

    Constraints are applied by generating all possible sample spaces using a cartesian product
    of values in the pips domain across all tiles. A condition is asserted onto the samples to
    filter valid samples.

    Valid conditions are {EQUAL_TO, GREATER_THAN, LESSER_THAN, ALL_EQUAL, ALL_NOT_EQUAL}

    Returns a callable function to apply the constraint to tiles related to the constraint.
    This callable takes a Tile object.
    '''
    # ------------------------------------------
    # VALIDATION
    # ------------------------------------------

    if not isinstance(condition, Condition):
        raise ValueError("Invalid condition")
    if not tiles:
        raise ValueError("No tiles were specified")
    
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
            raise ValueError(f"Specify a target value. Currently: {self.target_value}")
        
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
    
    # -----------------------------------------
    # PROCESS
    # -----------------------------------------

    # Build cartesian product of pips domains

    pips = [sorted(tile.pips.values) for tile in tiles]
    all_combinations = product(*pips)

    # Keep only combinations that satisfy the condition
    
    valid_combinations = [combination 
                          for combination in all_combinations 
                          if _satisfies(s=combination, target_value=target_value, condition=condition)
                          ]

    # For each tile, build the set of values that are valid

    positional_values = [set() for _ in tiles]
    for combination in valid_combinations:
        for index, value in enumerate(combination):
            positional_values[index].add(value)

    # Create reference dictionary, {tile : set(allowed values)}

    allowed_sets = dict(zip(tiles, positional_values))
    
    # ------------------------------------------
    # CURRIED FUNCTION TO MUTATE TILE(S)
    # ------------------------------------------
    
    def select_tile(tile: Tile) -> bool:
        if tile not in tiles:
            raise ValueError(f"Constraint is not related to {tile}")

        allowed_set = allowed_sets[tile]
        
        if allowed_set != tile.pips.values:
            has_changed =tile.pips.restrict_to(allowed_set) # mutation occurs
            if has_changed:
                update_dominoes(tile)
            return has_changed

        return False

    return select_tile


def exclude_domino(domino: Domino):
    # TODO: Write unit tests for this function
    def select_tile(tile: Tile) -> bool:
        has_changed = tile.dominoes.remove(domino)
        if has_changed:
            update_pips(tile)
        return has_changed
    return select_tile

def exclude_neighbour(neighbour: Tile):
    # TODO: Write unit tests for this function
    def select_tile(tile: Tile) -> bool:
        has_changed = tile.neighbours.remove(neighbour)
        return has_changed
    return select_tile

def restrict_dominoes(allowed_set: set[Domino]):
    # TODO: Write unit tests for this function
    def select_tile(tile: Tile) -> bool:
        has_changed = tile.dominoes.restrict_to(allowed_set)
        if has_changed:
            update_pips(tile)
        return has_changed
    return select_tile

def pair_tile(tile1: Tile):
    # TODO: Write unit tests for this function
    def select_tile(tile2: Tile) -> bool:
        return tile2.neighbours.restrict_to({tile1.id})
    return select_tile
