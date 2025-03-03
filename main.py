import tkinter as tk
from tgme.tmge import TMGE
from tgme.player_profile import PlayerProfile
from tgme.player import Player
from tgme.game import SampleMatchingGame
from games.tetris_game import TetrisGame
from games.puzzle_fighter_game import PuzzleFighterGame
from tgme.views.game_ui import GameUI
from tgme.views.login_window import LoginWindow
from tgme.views.home_window import HomeWindow

class TMGEApplication:
    def __init__(self) -> None:
        self.tmge = TMGE()
        self.tmge.start()
        self.current_profile = None
        self.game_controls_dict = {}

    def on_login_success(self, profile: PlayerProfile) -> None:
        self.current_profile = profile
        self.show_main_window()

    def show_main_window(self) -> None:
        # Create players for two-player games
        player1 = Player(self.current_profile)
        player2 = Player(PlayerProfile("Player2"))  # Temporary second player
        
        # Register games with two players
        tetris_game = TetrisGame(game_id='Tetris', players=[player1, player2], controls=self.game_controls_dict['Tetris'])
        puzzle_fighter = PuzzleFighterGame(game_id='Puzzle Fighter', players=[player1, player2], controls=self.game_controls_dict['PuzzleFighter'])
        
        self.tmge.register_game(tetris_game)
        self.tmge.register_game(puzzle_fighter)

        # Show home window
        home = HomeWindow(self.tmge, self.current_profile)
        home.window.mainloop()

    def quit_tmge(self) -> None:
        self.tmge.quit()
        if self.root:
            self.root.quit()
    
    def set_controls(self) -> None:
        # Tetris Game Controls
        self.game_controls_dict['Tetris'] = [
            {'left': 'a', 'right': 'd', 'down': 's', 'rotate': 'w', 'drop': 'space'},  # Player 1
            {'left': 'Left', 'right': 'Right', 'down': 'Down', 'rotate': 'Up', 'drop': 'Return'}   # Player 2
        ]

        # Puzzle Fighter Game Controls
        self.game_controls_dict['PuzzleFighter'] = [
            {'left': 'a', 'right': 'd', 'down': 's', 'rotate': 'w', 'counter_rotate': 'q'},
            {'left': 'Left', 'right': 'Right', 'down': 'Down', 'rotate': 'Up', 'counter_rotate': 'Delete'}
        ]

def main() -> None:
    app = TMGEApplication()
    login = LoginWindow(app.tmge, app.on_login_success)
    login.window.mainloop()

if __name__ == "__main__":
    main()