class GameStats:
    def __init__(self) -> None:
        """
        __init__

        Args:
            None

        Returns:
            None
        """
        self.high_score: int = 0
        self.games_played: int = 0
        self.wins: int = 0

    def update_score(self, score: int) -> None:
        """
        update_score

        Args:
            score (int): The new score to compare against the high score

        Returns:
            None
        """
        if score > self.high_score:
            self.high_score = score

    def increment_games_played(self) -> None:
        """
        increment_games_played

        Args:
            None

        Returns:
            None
        """
        self.games_played += 1

    def add_win(self) -> None:
        """
        add_win

        Args:
            None

        Returns:
            None
        """
        self.wins += 1 