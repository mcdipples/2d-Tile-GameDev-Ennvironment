from typing import List, Optional
from tgme.tile import Tile

class Grid:
    '''
    This class is responsible for the grid of the game.

    Each Grid has a list of tiles. Each Grid is to be implemented by the developer.

    Each Tile has a type and a state. 
    '''
    def __init__(self, rows: int, columns: int) -> None:
        """
        __init__

        Args:
            rows (int): The number of rows in the grid
            columns (int): The number of columns in the grid

        Returns:
            None
        """
        self.rows: int = rows
        self.columns: int = columns
        self.tiles: List[List[Optional[Tile]]] = [
            [None for _ in range(columns)] for _ in range(rows)
        ]

    #& NEW, to replace valid move logic in each game.
    def is_valid_move(self, x: int, y: int) -> bool:
        '''
        valid_move checks if the move is valid.
        '''
        return 0 <= x < self.rows and 0 <= y < self.columns
    
    #? FLOW: handle_keypress -> check_valid_move -> 
    #? place somewhere in grid -> use Tile.move() to actually change tile's position

    def place_tile(self, tile: Tile, x: int, y: int) -> None:
        """
        place_tile calls Tile.move()

        Args:
            tile (Tile): The tile to place
            x (int): Row index
            y (int): Column index

        Returns:
            None
        """
        if 0 <= x < self.rows and 0 <= y < self.columns:
            self.tiles[x][y] = tile

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """
        get_tile

        Args:
            x (int): Row index
            y (int): Column index

        Returns:
            tile (Optional[Tile]): Tile at that position, or None if out of bounds or empty
        """
        if 0 <= x < self.rows and 0 <= y < self.columns:
            return self.tiles[x][y]
        return None

    def check_matches(self) -> List[List[Tile]]:
        """
        check_matches

        Args:
            None

        Returns:
            matches (List[List[Tile]]): List of lists of matched tiles
        """
        # Placeholder for matching logic in a real game
        return []

    def clear_matches(self) -> None:
        """
        clear_matches removes all tiles that are matched based on the check_matches method.

        clearing logic is up to the developer to implement.

        (example: tetris clears lines, )

        Args:
            None

        Returns:
            None
        """
        # Placeholder for matching/clearing logic in a real game
        pass  