import random
from typing import List, Optional, Set, Tuple
import time
from tgme.game import Game
from tgme.player import Player
from tgme.tile import Tile
from tgme.grid import Grid
from games.puzzle_fighter_piece import PuzzleFighterPiece

class PuzzleFighterGame(Game):
    min_players = 1
    max_players = 2
    
    def __init__(self, game_id: str, players: List[Player], controls) -> None:
        super().__init__(game_id, 12, 6, players, controls=controls)
        
        # Create grids for each player
        self.grids = [Grid(12, 6) for _ in range(len(players))]
        self.current_pieces = [None] * len(players)
        self.scores = [0] * len(players)
        self.fall_times = [0] * len(players)
        self.fall_speed = 0.5
        self.last_falls = [time.time()] * len(players)
        self.game_over = [False] * len(players)
        self.combo_counters = [0] * len(players)
        
        # Controls are set in Game constructor
        # # Controls for each player
        # self.controls = [
        #     {'left': 'a', 'right': 'd', 'down': 's', 'rotate': 'w', 'counter_rotate': 'q'},
        #     {'left': 'Left', 'right': 'Right', 'down': 'Down', 'rotate': 'Up', 'counter_rotate': 'Delete'}
        # ]
        
        # Add attack queue
        self.pending_attacks = [[], []]  # List of rows to add for each player
        
        self.logger.debug("PuzzleFighter initialized with attack system")

    def initialize_game(self) -> None:
        """Start a new game"""
        self.current_pieces = [PuzzleFighterPiece() for _ in range(len(self.players))]
        self.scores = [0] * len(self.players)
        self.game_over = [False] * len(self.players)
        self.combo_counters = [0] * len(self.players)

    def _check_chain_reaction(self, player: int, crash_positions: Set[Tuple[int, int]]) -> None:
        """Check for chain reactions and generate attacks"""
        total_gems_cleared = 0
        while crash_positions:
            new_crashes = set()
            current_crashes = crash_positions
            crash_positions = set()

            # First, remove all gems in current crash positions
            for x, y in current_crashes:
                tile = self.grids[player].get_tile(y, x)
                if tile:
                    self.grids[player].tiles[y][x] = None
                    total_gems_cleared += 1

            # Then check for any gems that should fall
            self._apply_gravity(player)

            # Look for new matches after gems have fallen
            for y in range(self.grids[player].rows):
                for x in range(self.grids[player].columns):
                    tile = self.grids[player].get_tile(y, x)
                    if not tile or tile.tile_type != 'gem':
                        continue

                    # Check adjacent gems for matches
                    color = tile.tile_color
                    matches = self._find_adjacent_matches(player, x, y, color, set())
                    if len(matches) >= 3:  # Need at least 3 matching gems
                        crash_positions.update(matches)

            if crash_positions:
                self.combo_counters[player] += 1
                self.scores[player] += (100 * len(crash_positions) * self.combo_counters[player])

        # Generate attack based on chain size and combo
        if total_gems_cleared >= 4:
            # Reduce attack strength to be more balanced
            attack_rows = (total_gems_cleared // 5) + (self.combo_counters[player] // 3)
            attack_rows = min(attack_rows, 3)  # Cap maximum attack rows
            
            opponent = 1 if player == 0 else 0
            self.pending_attacks[opponent].extend(['gray'] * attack_rows)
            self.logger.info(f"Player {player + 1} sends {attack_rows} rows to opponent")

    def _find_adjacent_matches(self, player: int, x: int, y: int, color: str, visited: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        """Find all connected gems of the same color using flood fill"""
        if not (0 <= x < self.grids[player].columns and 0 <= y < self.grids[player].rows):
            return set()

        if (x, y) in visited:
            return set()

        tile = self.grids[player].get_tile(y, x)
        if not tile or tile.tile_color != color:
            return set()

        matches = {(x, y)}
        visited.add((x, y))

        # Check all adjacent positions
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            matches.update(self._find_adjacent_matches(player, x + dx, y + dy, color, visited))

        return matches

    def _apply_gravity(self, player: int) -> None:
        """Make gems fall to fill empty spaces"""
        for col in range(self.grids[player].columns):
            # Start from bottom, move gems down
            empty_row = self.grids[player].rows - 1
            for row in range(self.grids[player].rows - 1, -1, -1):
                if self.grids[player].get_tile(row, col):
                    if empty_row != row:
                        self.grids[player].tiles[empty_row][col] = self.grids[player].tiles[row][col]
                        self.grids[player].tiles[row][col] = None
                    empty_row -= 1

    def _process_power_gems(self, player: int) -> None:
        """Process power gems and their effects"""
        for y in range(self.grids[player].rows):
            for x in range(self.grids[player].columns):
                tile = self.grids[player].get_tile(y, x)
                if not tile or tile.tile_type != 'power':
                    continue
                    
                # Clear all gems of same color
                color = tile.tile_color
                crash_positions = set()
                
                for cy in range(self.grids[player].rows):
                    for cx in range(self.grids[player].columns):
                        check_tile = self.grids[player].get_tile(cy, cx)
                        if check_tile and check_tile.tile_color == color:
                            self.grids[player].tiles[cy][cx] = None
                            crash_positions.add((cx, cy))
                
                if crash_positions:
                    self.combo_counters[player] += 1
                    self._check_chain_reaction(player, crash_positions)

    def handle_key_press(self, event: object) -> None:
        """Handle input for both players"""
        key = getattr(event, 'keysym', None)
        if not key:
            return

        for player in range(len(self.players)):
            if not self.game_over[player] and self.current_pieces[player]:
                if key == self.controls[player]['left']:
                    self._move_piece(player, -1, 0)
                elif key == self.controls[player]['right']:
                    self._move_piece(player, 1, 0)
                elif key == self.controls[player]['down']:
                    self._move_piece(player, 0, 1)
                elif key == self.controls[player]['rotate']:
                    self._rotate_piece(player, True)
                elif key == self.controls[player]['counter_rotate']:
                    self._rotate_piece(player, False)

    def _move_piece(self, player: int, dx: int, dy: int) -> bool:
        piece = self.current_pieces[player]
        if not piece:
            return False

        piece.move(dx, dy)
        if not self._is_valid_position(player):
            piece.move(-dx, -dy)
            if dy > 0:
                self._freeze_piece(player)
            return False
        return True

    def _is_valid_position(self, player: int) -> bool:
        piece = self.current_pieces[player]
        if not piece:
            return False

        for x, y, _ in piece.get_positions:
            if not (0 <= x < self.grids[player].columns and y < self.grids[player].rows):
                return False
            if y >= 0 and self.grids[player].get_tile(y, x):
                return False
        return True

    def _rotate_piece(self, player: int, clockwise: bool) -> None:
        piece = self.current_pieces[player]
        if not piece:
            return

        if clockwise:
            piece.rotate_clockwise()
        else:
            for _ in range(3):  # Counter-clockwise is 3 clockwise rotations
                piece.rotate_clockwise()

        if not self._is_valid_position(player):
            # Try wall kicks
            for dx in [-1, 1]:
                piece.move(dx, 0)
                if self._is_valid_position(player):
                    return
                piece.move(-dx, 0)
            # Revert rotation if wall kicks fail
            if clockwise:
                for _ in range(3):
                    piece.rotate_clockwise()
            else:
                piece.rotate_clockwise()

    def _freeze_piece(self, player: int) -> None:
        """Freeze current piece and check for matches"""
        piece = self.current_pieces[player]
        if not piece:
            return

        # Place the gems
        for x, y, tile in piece.get_positions:
            if y >= 0:
                self.grids[player].place_tile(tile, y, x)

        # Apply gravity to make gems fall
        self._apply_gravity(player)

        # Check for power gems first
        self._process_power_gems(player)

        # Then check for normal matches
        for x, y in [(x, y) for x, y, _ in piece.get_positions]:
            if y >= 0:
                tile = self.grids[player].get_tile(y, x)
                if tile and tile.tile_type == 'gem':
                    matches = self._find_adjacent_matches(player, x, y, tile.tile_color, set())
                    if len(matches) >= 3:
                        self._check_chain_reaction(player, matches)

        # Create new piece if game isn't over
        if not self.game_over[player]:
            self.current_pieces[player] = PuzzleFighterPiece()
            # Check if new piece can be placed
            if not self._is_valid_position(player):
                self.game_over[player] = True
                self.logger.info(f"Player {player + 1} lost - board filled up!")

    def _process_attacks(self, player: int) -> None:
        """Process pending attacks for a player"""
        if not self.pending_attacks[player]:
            return

        # Check if there's room to add attack rows
        top_row_occupied = any(self.grids[player].get_tile(0, x) for x in range(self.grids[player].columns))
        if top_row_occupied:
            self.game_over[player] = True
            return

        # Get the next attack row
        attack_color = self.pending_attacks[player].pop(0)

        # Shift existing blocks up by one row
        for row in range(0, self.grids[player].rows - 1):
            for col in range(self.grids[player].columns):
                self.grids[player].tiles[row][col] = self.grids[player].tiles[row + 1][col]

        # Add attack row at bottom
        for col in range(self.grids[player].columns):
            # Add one gap randomly in the attack row
            if col == random.randint(0, self.grids[player].columns - 1):
                self.grids[player].tiles[self.grids[player].rows - 1][col] = None
            else:
                self.grids[player].place_tile(
                    Tile('block', 'locked', color=attack_color),
                    self.grids[player].rows - 1,
                    col
                )

    def update(self) -> None:
        """Update game state with attacks"""
        # Process pending attacks first
        for player in range(len(self.players)):
            if self.pending_attacks[player]:
                self._process_attacks(player)
        
        # Regular update
        current_time = time.time()
        for player in range(len(self.players)):
            if not self.game_over[player]:
                if current_time - self.last_falls[player] > self.fall_speed:
                    self._move_piece(player, 0, 1)
                    self.last_falls[player] = current_time

    def check_win_condition(self) -> bool:
        """Check if someone has won"""
        if all(self.game_over):
            winner = 0 if self.scores[0] >= self.scores[1] else 1
            self.logger.info(f"Player {winner + 1} wins with score {self.scores[winner]}")
            return True
        return False

    def check_loss_condition(self) -> bool:
        """Check if either player has lost"""
        for player in range(len(self.players)):
            # Check top row for blockage
            if not self.game_over[player]:
                for x in range(self.grids[player].columns):
                    if self.grids[player].get_tile(0, x):
                        self.game_over[player] = True
                        self.logger.info(f"Player {player + 1} lost - reached top!")
                        break

        return any(self.game_over)

    def handle_game_over(self) -> None:
        """Handle game over with custom message"""
        message = "Game Over!\n\n"
        if all(self.game_over):
            winner = 0 if self.scores[0] >= self.scores[1] else 1
            message += f"Player {winner + 1} wins!\nScore: {self.scores[winner]}"
        else:
            alive_player = 0 if not self.game_over[0] else 1
            message += f"Player {alive_player + 1} wins!\nScore: {self.scores[alive_player]}"

        if messagebox.askyesno("Game Over", message + "\n\nWould you like to restart?"):
            self.restart_game()
        else:
            self.exit_to_menu()
