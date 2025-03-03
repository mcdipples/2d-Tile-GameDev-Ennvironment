from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from tkinter import messagebox
from tgme.interfaces import IGameLoop, IInputHandler
from tgme.grid import Grid
from tgme.tile import Tile
from tgme.player import Player
from tgme.utils.logger import TMGELogger

class Game(IGameLoop, IInputHandler, ABC):
    def __init__(self, game_id: str, rows: int, columns: int, players: List[Player], controls: Dict) -> None:
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
        self.logger = TMGELogger()
        self.logger.info(f"Initializing game: {game_id}")
        
        # These should be set by child classes before calling super().__init__
        if not hasattr(self, 'min_players'):
            self.min_players = 1
        if not hasattr(self, 'max_players'):
            self.max_players = 1
            
        if not self.min_players <= len(players) <= self.max_players:
            raise ValueError(f"Game requires {self.min_players}-{self.max_players} players")

        self.game_id: str = game_id
        self.grid: Grid = Grid(rows, columns)
        self.players: List[Player] = players
        self.controls: Dict[int, Dict[str, str]] = controls
        self.is_paused = False
        self.is_game_over = False
        self.current_player_count = len(players)
        
        self.logger.debug(f"Created {rows}x{columns} grid for {game_id}")
        self.logger.debug(f"Registered {len(players)} players")

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

    @abstractmethod
    def check_loss_condition(self) -> bool:
        """Check if the game has been lost"""
        pass

    def handle_game_over(self) -> None:
        """Handle game over state with restart/exit options"""
        if messagebox.askyesno("Game Over", "Would you like to restart?"):
            self.restart_game()
        else:
            self.exit_to_menu()

    def restart_game(self) -> None:
        """Reset game state and start new game"""
        self.is_game_over = False
        self.is_paused = False
        self.initialize_game()
        self.logger.info(f"Restarting game: {self.game_id}")

    def exit_to_menu(self) -> None:
        """Clean up and exit to main menu"""
        self.is_game_over = True
        self.logger.info(f"Exiting game: {self.game_id}")

    def pause_game(self) -> None:
        """Toggle game pause state"""
        self.is_paused = not self.is_paused
        state = "paused" if self.is_paused else "resumed"
        self.logger.info(f"Game {state}: {self.game_id}")

    def init(self) -> None:
        """
        init

        Args:
            None

        Returns:
            None
        """
        self.logger.info(f"Starting game: {self.game_id}")
        self.initialize_game()

    def update(self) -> None:
        """
        update

        Args:
            None

        Returns:
            None
        """
        if self.is_paused or self.is_game_over:
            return

        if self.check_loss_condition():
            self.is_game_over = True
            self.handle_game_over()
        elif self.check_win_condition():
            self.is_game_over = True
            messagebox.showinfo("Congratulations", "You won!")
            self.handle_game_over()

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
        key = getattr(event, 'keysym', None)
        if key:
            self.logger.debug(f"Key pressed: {key}")

    def handle_key_release(self, event: object) -> None:
        """
        handle_key_release

        Args:
            event (object): Key event or similar input object

        Returns:
            None
        """
        key = getattr(event, 'keysym', None)
        if key:
            self.logger.debug(f"Key released: {key}")


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