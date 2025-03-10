from typing import List
from tgme.tile import Tile
from tgme.grid import Grid
from tgme.interfaces import IMatchingStrategy

class TetrisMatchingStrategy(IMatchingStrategy):
    def match(self, grid: Grid) -> List[int]:
        """
        Check for full lines in the grid and return a list of row indices that are fully filled.
        """
        full_lines = []

        # Iterate over the grid rows from top to bottom
        for y in range(grid.rows):
            if all(grid.get_tile(y, x) is not None for x in range(grid.columns)):
                full_lines.append(y)

        return full_lines