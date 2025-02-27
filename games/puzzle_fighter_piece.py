from typing import List, Tuple
import random
from tgme.tile import Tile, TileShape

class PuzzleFighterPiece:
    COLORS = ['red', 'blue', 'green', 'yellow']
    TYPES = ['gem', 'crash', 'power']
    
    def __init__(self) -> None:
        # Create main gem
        self.main_color = random.choice(self.COLORS)
        self.is_power = random.random() < 0.1  # 10% chance for power gem
        
        # Create connector gem (always regular gem)
        self.sub_color = random.choice(self.COLORS)
        
        # Position in grid
        self.x = 3  # Center of board
        self.y = 0  # Top of board
        self.connector_position = 'right'  # right, down
        
        # Create tile objects
        self.main_tile = Tile(
            'power' if self.is_power else 'gem',
            'active',
            color=self.main_color
        )
        self.sub_tile = Tile('gem', 'active', color=self.sub_color)

    def rotate_clockwise(self) -> None:
        """Rotate the connector gem clockwise around main gem"""
        if self.connector_position == 'right':
            self.connector_position = 'down'
        elif self.connector_position == 'down':
            self.connector_position = 'left'
        elif self.connector_position == 'left':
            self.connector_position = 'up'
        else:  # up
            self.connector_position = 'right'

    def get_positions(self) -> List[Tuple[int, int, Tile]]:
        """Get positions of both gems as (x, y, tile) tuples"""
        positions = [(self.x, self.y, self.main_tile)]
        
        if self.connector_position == 'right':
            positions.append((self.x + 1, self.y, self.sub_tile))
        elif self.connector_position == 'down':
            positions.append((self.x, self.y + 1, self.sub_tile))
        elif self.connector_position == 'left':
            positions.append((self.x - 1, self.y, self.sub_tile))
        else:  # up
            positions.append((self.x, self.y - 1, self.sub_tile))
            
        return positions

    def move(self, dx: int, dy: int) -> None:
        """Move the piece"""
        self.x += dx
        self.y += dy
