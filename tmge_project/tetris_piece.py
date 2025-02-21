from typing import List, Tuple
import random

class TetrisPiece:
    # Define tetromino shapes as lists of (x,y) coordinates
    SHAPES = {
        'I': [(0,0), (0,1), (0,2), (0,3)],
        'O': [(0,0), (1,0), (0,1), (1,1)],
        'T': [(0,0), (1,0), (2,0), (1,1)],
        'L': [(0,0), (0,1), (0,2), (1,2)],
        'J': [(1,0), (1,1), (1,2), (0,2)],
        'S': [(0,1), (1,1), (1,0), (2,0)],
        'Z': [(0,0), (1,0), (1,1), (2,1)]
    }

    COLORS = {
        'I': 'cyan',
        'O': 'yellow',
        'T': 'purple',
        'L': 'orange',
        'J': 'blue',
        'S': 'green',
        'Z': 'red'
    }

    def __init__(self) -> None:
        self.shape = random.choice(list(self.SHAPES.keys()))
        self.coords = self.SHAPES[self.shape][:]
        self.color = self.COLORS[self.shape]
        self.x = 4  # Starting x position (center of board)
        self.y = 0  # Starting y position (top of board)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    def rotate(self) -> None:
        # Rotate piece clockwise around (0,0)
        self.coords = [(y, -x) for (x, y) in self.coords]

    def get_positions(self) -> List[Tuple[int, int]]:
        # Return actual board positions of piece
        return [(self.x + x, self.y + y) for (x, y) in self.coords]
