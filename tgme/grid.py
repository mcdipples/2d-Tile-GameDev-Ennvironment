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

    def is_valid_movement(self, tile: Tile, new_x: int, new_y: int) -> bool:
        """Check if a tile can move to a new position"""
        # Check bounds
        if not (0 <= new_x < self.columns and 0 <= new_y < self.rows):
            return False
            
        # Check collision with other tiles
        for y in range(tile.tile_shape.height):
            for x in range(tile.tile_shape.width):
                if tile.tile_shape.pattern[y][x]:
                    grid_x, grid_y = new_x + x, new_y + y
                    if not self.is_valid_position(grid_x, grid_y):
                        return False
                    existing_tile = self.get_tile(grid_y, grid_x)
                    if existing_tile and existing_tile != tile:
                        return False
        
        return True