from typing import List, Optional, Tuple
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
        if rows <= 0 or columns <= 0:
            raise ValueError("Grid dimensions must be positive integers")
            
        self.rows: int = rows
        self.columns: int = columns
        self.tiles: List[List[Optional[Tile]]] = [
            [None for _ in range(columns)] for _ in range(rows)
        ]

    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if a position is within grid bounds"""
        return 0 <= x < self.rows and 0 <= y < self.columns

    def place_tile(self, tile: Tile, x: int, y: int) -> bool:
        """
        place_tile calls Tile.move()

        Args:
            tile (Tile): The tile to place
            x (int): Row index
            y (int): Column index

        Returns:
            bool: True if the tile was placed, False otherwise
        """
        if not isinstance(tile, Tile):
            raise TypeError("Expected Tile object")
            
        if not self.is_valid_position(x, y):
            return False
            
        self.tiles[x][y] = tile
        return True

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """
        get_tile

        Args:
            x (int): Row index
            y (int): Column index

        Returns:
            tile (Optional[Tile]): Tile at that position, or None if out of bounds or empty
        """
        if not self.is_valid_position(x, y):
            return None
        return self.tiles[x][y]

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