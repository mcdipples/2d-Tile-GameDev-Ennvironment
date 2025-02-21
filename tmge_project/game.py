from abc import ABC, abstractmethod
from typing import List
from interfaces import IGameLoop, IInputHandler
from grid import Grid
from player import Player

class Game(IGameLoop, IInputHandler, ABC):
    def __init__(self, game_id: str, rows: int, columns: int, players: List[Player]) -> None:
        """
        __init__

        Args:
            game_id (str): Unique identifier for the game
            rows (int): Number of rows in the grid
            columns (int): Number of columns in the grid
            players (List[Player]): The players participating in the game

        Returns:
            None
        """
        self.game_id: str = game_id
        self.grid: Grid = Grid(rows, columns)
        self.players: List[Player] = players

    @abstractmethod
    def initialize_game(self) -> None:
        """
        initialize_game

        Args:
            None

        Returns:
            None
        """
        pass

    @abstractmethod
    def check_win_condition(self) -> bool:
        """
        check_win_condition

        Args:
            None

        Returns:
            result (bool): Whether a player has won
        """
        pass

    def init(self) -> None:
        """
        init

        Args:
            None

        Returns:
            None
        """
        self.initialize_game()

    def update(self) -> None:
        """
        update

        Args:
            None

        Returns:
            None
        """
        # Placeholder for game loop logic
        pass

    def draw(self) -> None:
        """
        draw

        Args:
            None

        Returns:
            None
        """
        # Placeholder for rendering logic in a GUI
        pass

    def handle_key_press(self, event: object) -> None:
        """
        handle_key_press

        Args:
            event (object): Key event or similar input object

        Returns:
            None
        """
        # Handle key presses
        pass

    def handle_key_release(self, event: object) -> None:
        """
        handle_key_release

        Args:
            event (object): Key event or similar input object

        Returns:
            None
        """
        # Handle key releases
        pass


class SampleMatchingGame(Game):
    def initialize_game(self) -> None:
        """
        initialize_game

        Args:
            None

        Returns:
            None
        """
        # Example: place some tiles, reset player scores, etc.
        print(f'Initializing {self.game_id} with a {self.grid.rows}x{self.grid.columns} grid.')
        import random
        for row in range(self.grid.rows):
            for col in range(self.grid.columns):
                tile_type = random.randint(0, 4)  # 5 different tile types
                tile = Tile(tile_type, "active")
                self.grid.place_tile(tile, row, col)
        
        self.selected_tile = None
        self.cursor_pos = [0, 0]  # [row, col]

    def check_win_condition(self) -> bool:
        """
        check_win_condition

        Args:
            None

        Returns:
            result (bool): True if game is won, False otherwise
        """
        # Logic to determine if a match condition is met
        return False

    def handle_key_press(self, event: object) -> None:
        """
        handle_key_press

        Args:
            event (object): Key event or similar input object

        Returns:
            None
        """
        key = getattr(event, 'keysym', None)
        if not key:
            return

        if key == 'Up' and self.cursor_pos[0] > 0:
            self.cursor_pos[0] -= 1
        elif key == 'Down' and self.cursor_pos[0] < self.grid.rows - 1:
            self.cursor_pos[0] += 1
        elif key == 'Left' and self.cursor_pos[1] > 0:
            self.cursor_pos[1] -= 1
        elif key == 'Right' and self.cursor_pos[1] < self.grid.columns - 1:
            self.cursor_pos[1] += 1
        elif key == 'space':
            self.handle_tile_selection()

    def handle_tile_selection(self) -> None:
        """
        handle_tile_selection

        Args:
            None

        Returns:
            None
        """
        current_tile = self.grid.get_tile(self.cursor_pos[0], self.cursor_pos[1])
        
        if not current_tile:
            return

        if not self.selected_tile:
            self.selected_tile = (self.cursor_pos[0], self.cursor_pos[1])
        else:
            # Try to swap tiles
            row1, col1 = self.selected_tile
            row2, col2 = self.cursor_pos
            self.swap_tiles(row1, col1, row2, col2)
            self.selected_tile = None

    def swap_tiles(self, row1: int, col1: int, row2: int, col2: int) -> None:
        """
        swap_tiles

        Args:
            row1 (int): Row of the first tile
            col1 (int): Column of the first tile
            row2 (int): Row of the second tile
            col2 (int): Column of the second tile

        Returns:
            None
        """
        tile1 = self.grid.get_tile(row1, col1)
        tile2 = self.grid.get_tile(row2, col2)
        
        if tile1 and tile2:
            self.grid.place_tile(tile1, row2, col2)
            self.grid.place_tile(tile2, row1, col1)
            
            # Update player score based on matches
            if self.check_matches():
                self.players[0].update_score(10)  # Simple scoring

    def check_matches(self) -> bool:
        """
        check_matches

        Args:
            None

        Returns:
            result (bool): True if matches are found, False otherwise
        """
        # Simple horizontal match check
        matches_found = False
        for row in range(self.grid.rows):
            for col in range(self.grid.columns - 2):
                tile1 = self.grid.get_tile(row, col)
                tile2 = self.grid.get_tile(row, col + 1)
                tile3 = self.grid.get_tile(row, col + 2)
                if tile1 and tile2 and tile3:
                    if tile1.is_matching(tile2) and tile2.is_matching(tile3):
                        self.grid.tiles[row][col] = None
                        self.grid.tiles[row][col + 1] = None
                        self.grid.tiles[row][col + 2] = None
                        matches_found = True
        return matches_found

    def update(self) -> None:
        """
        update

        Args:
            None

        Returns:
            None
        """
        # Handle tile falling
        for col in range(self.grid.columns):
            for row in range(self.grid.rows - 1, 0, -1):
                if not self.grid.get_tile(row, col):
                    # Move tile from above down
                    self.grid.tiles[row][col] = self.grid.tiles[row - 1][col]
                    self.grid.tiles[row - 1][col] = None