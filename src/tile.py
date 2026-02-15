from domino import Domino

class Tile:
    '''
    Tiles are parts of the gameboard where a domino can be placed. A single Domino spans two Tiles.
    A Tile contains domains of possible attributes:
    - neighbours: a set of tiles that may be linked by a domino
    - dominoes: a set of valid dominoes that may be placed in the tile
    - values: a set of possible values that the tile may have. This helps track orientation of the domino.
    '''
    def __init__(self, id: str, neighbours: set[str], dominoes: set[Domino]):
        self.id = id
        self.neighbours = neighbours
        self.dominoes = dominoes
        self.values = {v for d in dominoes for v in d.values}

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.id == other.id
        return NotImplemented

    def is_singleton(self, attribute: str = 'all') -> bool:
        valid_attributes = ['neighbours', 'dominoes', 'values', 'all']
        
        if attribute not in valid_attributes:
            raise ValueError(f"Attribute must be one of: {valid_attributes}")

        neighbours_is_singleton = len(self.neighbours) == 1
        dominoes_is_singleton = len(self.dominoes) == 1
        values_is_singleton = len(self.values) == 1

        if attribute == 'neighbours':
            return neighbours_is_singleton
        if attribute == 'dominoes':
            return dominoes_is_singleton
        if attribute == 'values':
            return values_is_singleton

        # attribute is 'all' or default
        return neighbours_is_singleton and dominoes_is_singleton and values_is_singleton
