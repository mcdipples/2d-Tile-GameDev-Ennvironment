from typing import List, Optional
import time
from tgme.game import Game
from tgme.player import Player
from tgme.tile import Tile
from games.tetris_piece import TetrisPiece
from tgme.grid import Grid

class TetrisGame(Game):
    def __init__(self, game_id: str, players: List[Player]) -> None:
        # Call parent class constructor first
        super().__init__(game_id, 20, 10, players)
        
        # Create two separate grids for two players
        self.grids = [Grid(20, 10), Grid(20, 10)]  # One grid per player
        self.current_pieces = [None, None]  # One piece per player
        self.scores = [0, 0]  # Score for each player
        self.fall_times = [0, 0]
        self.fall_speed = 0.5
        self.last_falls = [time.time(), time.time()]
        self.game_over = [False, False]
        
        # Player-specific controls
        self.controls = [
            {'left': 'a', 'right': 'd', 'down': 's', 'rotate': 'w', 'drop': 'space'},  # Player 1
            {'left': 'Left', 'right': 'Right', 'down': 'Down', 'rotate': 'Up', 'drop': 'Return'}   # Player 2
        ]
        
        self.logger.debug("TetrisGame initialized with 2-player setup")

    def initialize_game(self) -> None:
        self.current_pieces = [TetrisPiece(), TetrisPiece()]
        self.scores = [0, 0]
        self.game_over = [False, False]

    def handle_key_press(self, event: object) -> None:
        key = getattr(event, 'keysym', None)
        if not key or all(self.game_over):
            return

        # Handle player 1 controls (WASD + space)
        if not self.game_over[0]:
            if key == self.controls[0]['left']:
                self._move_piece(0, -1, 0)
            elif key == self.controls[0]['right']:
                self._move_piece(0, 1, 0)
            elif key == self.controls[0]['down']:
                self._move_piece(0, 0, 1)
            elif key == self.controls[0]['rotate']:
                self._rotate_piece(0)
            elif key == self.controls[0]['drop']:
                self._hard_drop(0)

        # Handle player 2 controls (Arrow keys + return)
        if not self.game_over[1]:
            if key == self.controls[1]['left']:
                self._move_piece(1, -1, 0)
            elif key == self.controls[1]['right']:
                self._move_piece(1, 1, 0)
            elif key == self.controls[1]['down']:
                self._move_piece(1, 0, 1)
            elif key == self.controls[1]['rotate']:
                self._rotate_piece(1)
            elif key == self.controls[1]['drop']:
                self._hard_drop(1)

    #TODO: implement piece movement logic with Grid.place_tile() and Grid.get_tile()
    def _move_piece(self, player: int, dx: int, dy: int) -> bool:
        if not self.current_pieces[player]:
            return False

        self.current_pieces[player].move(dx, dy)
        if not self._is_valid_move(player):
            self.current_pieces[player].move(-dx, -dy)
            if dy > 0:  # If moving down, piece is stuck
                self._freeze_piece(player)
                self._clear_lines(player)
                self.current_pieces[player] = TetrisPiece()
                if not self._is_valid_move(player):
                    self.game_over[player] = True
            return False
        return True

    def _is_valid_move(self, player: int) -> bool:
        if not self.current_pieces[player]:
            return False

        for x, y in self.current_pieces[player].get_positions():
            if not (0 <= x < self.grids[player].columns and y < self.grids[player].rows):
                return False
            if y >= 0 and self.grids[player].get_tile(y, x):
                return False
        return True

    def _rotate_piece(self, player: int) -> None:
        if not self.current_pieces[player]:
            return

        self.current_pieces[player].rotate()
        if not self._is_valid_move(player):
            # Try wall kicks
            for dx in [-1, 1, -2, 2]:
                self.current_pieces[player].move(dx, 0)
                if self._is_valid_move(player):
                    return
                self.current_pieces[player].move(-dx, 0)
            self.current_pieces[player].rotate()
            self.current_pieces[player].rotate()
            self.current_pieces[player].rotate()

    def _hard_drop(self, player: int) -> None:
        while self._move_piece(player, 0, 1):
            pass

    def _freeze_piece(self, player: int) -> None:
        if not self.current_pieces[player]:
            return

        for x, y in self.current_pieces[player].get_positions():
            if y >= 0:
                tile = Tile(self.current_pieces[player].color, "locked")
                self.grids[player].place_tile(tile, y, x)

    def _clear_lines(self, player: int) -> None:
        lines_cleared = 0
        y = self.grids[player].rows - 1
        while y >= 0:
            if all(self.grids[player].get_tile(y, x) for x in range(self.grids[player].columns)):
                # Move all lines above down
                for y2 in range(y - 1, -1, -1):
                    for x in range(self.grids[player].columns):
                        self.grids[player].tiles[y2 + 1][x] = self.grids[player].tiles[y2][x]
                # Clear top line
                for x in range(self.grids[player].columns):
                    self.grids[player].tiles[0][x] = None
                lines_cleared += 1
            else:
                y -= 1

        if lines_cleared:
            self.scores[player] += [100, 300, 500, 800][lines_cleared - 1]
            self.players[player].update_score(self.scores[player])

    def update(self) -> None:
        current_time = time.time()
        for player in range(2):
            if not self.game_over[player] and current_time - self.last_falls[player] > self.fall_speed:
                self._move_piece(player, 0, 1)
                self.last_falls[player] = current_time

    def check_win_condition(self) -> bool:
        return all(self.game_over)
