import tkinter as tk
from tmge import TMGE
from player_profile import PlayerProfile
from player import Player
from game import SampleMatchingGame
from tetris_game import TetrisGame
from game_ui import GameUI
from login_window import LoginWindow
from home_window import HomeWindow

class TMGEApplication:
    def __init__(self) -> None:
        self.tmge = TMGE()
        self.tmge.start()
        self.current_profile = None

    def on_login_success(self, profile: PlayerProfile) -> None:
        self.current_profile = profile
        self.show_main_window()

    def show_main_window(self) -> None:
        # Create players for two-player games
        player1 = Player(self.current_profile)
        player2 = Player(PlayerProfile("Player2"))  # Temporary second player
        
        # Register games with two players
        tetris_game = TetrisGame(game_id='Tetris', players=[player1, player2])
        self.tmge.register_game(tetris_game)

        # Show home window
        home = HomeWindow(self.tmge, self.current_profile)
        home.window.mainloop()

    def quit_tmge(self) -> None:
        self.tmge.quit()
        if self.root:
            self.root.quit()

def main() -> None:
    app = TMGEApplication()
    login = LoginWindow(app.tmge, app.on_login_success)
    login.window.mainloop()

if __name__ == "__main__":
    main()