from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from tkinter import messagebox
from tgme.interfaces import IGameLoop, IInputHandler
from tgme.grid import Grid
from tgme.tile import Tile
from tgme.interfaces import IMatchingStrategy
from tgme.player import Player
from tgme.utils.logger import TMGELogger

class Game(IGameLoop, IInputHandler, ABC):
    def __init__(self, game_id: str, rows: int, columns: int, players: List[Player], controls: Dict, matching_strategy: IMatchingStrategy) -> None:
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
        self.matching_strategy = matching_strategy
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