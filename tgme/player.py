from tgme.player_profile import PlayerProfile
from typing import Optional

class Player:
    def __init__(self, profile: PlayerProfile) -> None:
        """
        __init__

        Args:
            profile (PlayerProfile): The profile associated with this player

        Returns:
            None
        """
        self.profile: PlayerProfile = profile
        self.score: int = 0

    def update_score(self, points: int) -> None:
        """
        update_score

        Args:
            points (int): Points to add to the player's score

        Returns:
            None
        """
        self.score += points 