import abc
from abc import ABC
from typing import Protocol

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