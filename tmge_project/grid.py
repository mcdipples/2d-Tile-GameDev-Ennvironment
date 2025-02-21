from typing import List, Optional
from tile import Tile

class Grid:
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

    def place_tile(self, tile: Tile, x: int, y: int) -> None:
        """
        place_tile

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

    def clear_matches(self) -> None:
        """
        clear_matches

        Args:
            None

        Returns:
            None
        """
        # Placeholder for matching/clearing logic in a real game
        pass 