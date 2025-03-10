from tgme.interfaces import IMatchingStrategy
from games.tetris_matching_strategy import TetrisMatchingStrategy
from games.puzzle_fighter_matching_strategy import PuzzleFighterMatchingStrategy


class MatchingStrategyFactory:
    @staticmethod
    def get_strategy(game_id: str) -> IMatchingStrategy:
        """
        Factory method to return the correct matching strategy based on the game type.
        :param game_id: the game identifier to determine the strategy.
        :return: an appropriate instance of IMatchingStrategy.
        """
        if game_id == "Tetris":
            return TetrisMatchingStrategy()
        elif game_id == "Puzzle Fighter":
            return PuzzleFighterMatchingStrategy()
        else:
            raise ValueError(f"Unknown game type: {game_id}")
