from typing import Dict
from game_stats import GameStats

class PlayerProfile:
    def __init__(self, username: str) -> None:
        """
        __init__

        Args:
            username (str): The player's username

        Returns:
            None
        """
        self.username: str = username
        self.stats: Dict[str, GameStats] = {}

    def login(self, username: str) -> None:
        """
        login

        Args:
            username (str): The username to log in with

        Returns:
            None
        """
        # In a real implementation, you'd verify credentials.
        self.username = username

    def update_stats(self, game_id: str, stats: GameStats) -> None:
        """
        update_stats

        Args:
            game_id (str): The identifier of the game
            stats (GameStats): The updated game stats

        Returns:
            None
        """
        self.stats[game_id] = stats 