from .domino import Domino
from .domain import Domain

def all_dominoes() -> set[Domino]:
    return {Domino(i,j) for i in range(7) for j in range(i, 7)}


class Tile:
    '''
    Tiles are parts of the gameboard where a domino can be placed. A single Domino spans two Tiles.
    A Tile contains domains of possible attributes:
    - neighbours: a set of tiles that may be linked by a domino
    - dominoes: a set of valid dominoes that may be placed in the tile
    - values: a set of possible values that the tile may have. This helps track orientation of the domino.
    '''
    def __init__(self, id: str, neighbours: set[str], dominoes: set[Domino] = all_dominoes()):
        self.id = id
        self.neighbours = Domain(neighbours)
        self.dominoes = Domain(dominoes)
        self.pips = Domain({v for d in dominoes for v in d.values})

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.id == other.id
        return NotImplemented

    @property
    def is_singleton(self):
        return self.neighbours.is_singleton and self.dominoes.is_singleton and self.pips.is_singleton
    
    def __str__(self):
        return f"Tile(id={self.id}, neighbours={self.neighbours.values}, pips={self.pips.values}, count_dominoes={self.dominoes.size})"
    
    def __repr__(self):
        return self.__str__()
