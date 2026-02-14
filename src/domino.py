class Domino:
    '''
    A two sided game-piece. 
    Each side has a set of pips that represent the sides of a 6-sided die. This includes an option for no pips (0).
    This has been represented with an immutable set of these pips. It has been modelled independent of orientation.
    Contains the following features:
    - ability to compare dominoes to check if they are the same.
    - hashed so they can be used in set operations.
    - human-readable display when printed "[a, b]".
    '''
    def __init__(self, a: int, b: int):
        
        valid_values = {a, b}.issubset((range(7)))

        if not valid_values:
            raise ValueError("Dominoes can only contain values 0 to 6")

        self.values = frozenset((a, b))

    def __eq__(self, other):
        return self.values == other.values

    def __hash__(self):
        return hash(self.values)

    def __str__(self):
        return f"[{min(self.values)}, {max(self.values)}]"
