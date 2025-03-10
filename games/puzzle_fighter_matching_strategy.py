from typing import List, Set, Tuple
from tgme.tile import Tile
from tgme.grid import Grid
from tgme.interfaces import IMatchingStrategy

class PuzzleFighterMatchingStrategy(IMatchingStrategy):
    def match(self, grid: Grid) -> List[List[Tile]]:
        """Find all matches of at least 3 adjacent tiles with the same color"""
        matched_tiles = []
        visited = set()

        for y in range(grid.rows):
            for x in range(grid.columns):
                if (x, y) in visited:
                    continue
                
                tile = grid.get_tile(y, x)
                if tile and tile.tile_type == 'gem':
                    matches = self._find_adjacent_matches(grid, x, y, tile.tile_color, visited)
                    if len(matches) >= 3:
                        matched_tiles.append([grid.get_tile(y, x) for (x, y) in matches])
                        visited.update(matches)

        return matched_tiles

    def _find_adjacent_matches(self, grid: Grid, x: int, y: int, color: str, visited: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        """Find all connected gems of the same color using flood fill"""
        if not (0 <= x < grid.columns and 0 <= y < grid.rows):
            return set()

        if (x, y) in visited:
            return set()

        tile = grid.get_tile(y, x)
        if not tile or tile.tile_color != color:
            return set()

        matches = {(x, y)}
        visited.add((x, y))

        # Check all adjacent positions
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            matches.update(self._find_adjacent_matches(grid, x + dx, y + dy, color, visited))

        return matches