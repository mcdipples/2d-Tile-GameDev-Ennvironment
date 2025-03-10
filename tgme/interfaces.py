import abc
from abc import ABC
from typing import List
from tgme.tile import Tile

class IGameManager(ABC):
    def manage_games(self) -> None:
        self.start()
        self.quit()
    
    @abc.abstractmethod
    def start(self) -> None:
        """
        start

        Args:
            None

        Returns:
            None
        """
        pass

    @abc.abstractmethod
    def quit(self) -> None:
        """
        quit

        Args:
            None

        Returns:
            None
        """
        pass


class IGameLoop(ABC):
    @abc.abstractmethod
    def init(self) -> None:
        """
        init

        Args:
            None

        Returns:
            None
        """
        pass

    @abc.abstractmethod
    def update(self) -> None:
        """
        update

        Args:
            None

        Returns:
            None
        """
        pass

    @abc.abstractmethod
    def draw(self) -> None:
        """
        draw

        Args:
            None

        Returns:
            None
        """
        pass


class IInputHandler(ABC):
    @abc.abstractmethod
    def handle_key_press(self, event: object) -> None:
        """
        handle_key_press

        Args:
            event (object): Key event or similar input object

        Returns:
            None
        """
        pass

    @abc.abstractmethod
    def handle_key_release(self, event: object) -> None:
        """
        handle_key_release

        Args:
            event (object): Key event or similar input object

        Returns:
            None
        """
        pass 

class IMatchingStrategy(ABC):
    @abc.abstractmethod
    def match(self, grid: 'Grid') -> List[List[Tile]]:
        """
        Abstract method for matching tiles based on game-specific logic.

        Args:
            grid (Grid): The grid of the current game.

        Returns:
            List[List[Tile]]: A list of matched tiles that meet the matching criteria.
        """
        pass
