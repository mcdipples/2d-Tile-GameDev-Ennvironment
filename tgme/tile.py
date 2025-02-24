from typing import Any

class Tile:
    def __init__(self, tile_type: Any, tile_state: Any) -> None:
        """
        __init__

        Args:
            tile_type (Any): The type of the tile (e.g., color, shape)
            tile_state (Any): The state of the tile (active, cleared, etc.)

        Returns:
            None
        """
        self.tile_type = tile_type
        self.tile_state = tile_state

    def is_matching(self, other: 'Tile') -> bool:
        """
        is_matching

        Args:
            other (Tile): Another tile to compare with

        Returns:
            result (bool): True if they match based on type, False otherwise
        """
        return self.tile_type == other.tile_type 