import json

from ConstraintSolver.constructor import Gamedata
from ConstraintSolver.solver import Solver

def main():
    FILENAME = "games/medium_20260326.json"
    
    try:
        with open(FILENAME, "r") as f:
            game_data = json.load(f)
    except FileNotFoundError:
        print(f"File {FILENAME} not found.")
        game_data = None
    
    initial_game_state = Gamedata(game_data)
    
    game = Solver(initial_game_state)
    print("Initial Game State:")
    print(game)
    
    game.advance()
    print("Game Advanced 1:")
    print(game)
    
    game.advance()
    print("Game Advanced 2:")
    print(game)
    
    game.advance()
    print("Game Advanced 3:")
    print(game)


if __name__ == "__main__":
    main()
