from typing import Any, Tuple, Optional
from dataclasses import dataclass

@dataclass
class TileShape:
    width: int
    height: int
    pattern: list[list[bool]]  # True represents filled cell

class Tile:
    def __init__(self, tile_type: Any, tile_state: str, 
                 shape: Optional[TileShape] = None, 
                 color: str = 'gray') -> None:
        """
        __init__

        Args:
            tile_type (Any): The type of the tile (e.g., color, shape)
            tile_state (str): The state of the tile (active, cleared, etc.)
            shape (Optional[TileShape]): The shape of the tile
            color (str): The color of the tile

        Returns:
            None
        """
        self.tile_type = tile_type
        self.tile_state = tile_state
        self.tile_shape = shape or TileShape(1, 1, [[True]])  # Default 1x1 shape
        self.tile_color = color
        self.position: Tuple[int, int] = (0, 0)  # (x, y) top-left corner

    def set_position(self, x: int, y: int) -> None:
        self.position = (x, y)

    @property
    def get_position(self) -> Tuple[int, int]:
        return self.position

    def is_matching(self, other: 'Tile') -> bool:
        """
        is_matching

        Args:
            other (Tile): Another tile to compare with

        Returns:
            result (bool): True if they match based on type and color, False otherwise
        """
        return (self.tile_type == other.tile_type and 
                self.tile_color == other.tile_color)

    def occupies_position(self, x: int, y: int) -> bool:
        """Check if the tile's shape occupies a given position"""
        rel_x = x - self.position[0]
        rel_y = y - self.position[1]
        if 0 <= rel_x < self.tile_shape.width and 0 <= rel_y < self.tile_shape.height:
            return self.tile_shape.pattern[rel_y][rel_x]
        return False