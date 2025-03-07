from typing import List, Optional, Tuple, Set
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

    def check_tile_matches(self, min_match: int = 3) -> List[List[Tile]]:
        """Check for matching tiles in rows, columns, and diagonals"""
        matches: List[List[Tile]] = []
        
        # Check rows
        for row in range(self.rows):
            matches.extend(self._find_matches_in_line(
                [self.get_tile(row, col) for col in range(self.columns)],
                min_match
            ))
        
        # Check columns
        for col in range(self.columns):
            matches.extend(self._find_matches_in_line(
                [self.get_tile(row, col) for row in range(self.rows)],
                min_match
            ))

        return matches

    def _find_matches_in_line(self, line: List[Optional[Tile]], min_match: int) -> List[List[Tile]]:
        """Find sequences of matching tiles in a line"""
        matches = []
        current_match = []
        
        for tile in line:
            if not tile or not current_match:
                current_match = [tile] if tile else []
                continue
                
            if tile.is_matching(current_match[-1]):
                current_match.append(tile)
            else:
                if len(current_match) >= min_match:
                    matches.append(current_match)
                current_match = [tile]
        
        if len(current_match) >= min_match:
            matches.append(current_match)
            
        return matches

    def clear_matches(self, matches: List[List[Tile]]) -> int:
        """Clear matched tiles and return points earned"""
        cleared_count = 0
        for match in matches:
            for tile in match:
                pos = tile.get_position()
                self.tiles[pos[1]][pos[0]] = None
                cleared_count += 1
        return cleared_count

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