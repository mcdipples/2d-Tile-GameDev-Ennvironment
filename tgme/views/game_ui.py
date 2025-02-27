import tkinter as tk
from typing import Optional, List, Tuple, Any
from tgme.game import Game
from tgme.grid import Grid
from tgme.tile import Tile

class GameUI:
    '''
    This class is responsible for drawing the game UI.
    '''
    def __init__(self, root: tk.Tk, game: Game) -> None:
        self.root = root
        self.game = game
        self.canvas: Optional[tk.Canvas] = None
        self.cell_size = 30  # Slightly smaller to fit both boards
        self.padding = 50  # Space between boards
        self.init_ui()

    def init_ui(self) -> None:
        if hasattr(self.game, 'grids'):  # Two-player Tetris
            width = (self.game.grids[0].columns * self.cell_size * 2) + self.padding
            height = self.game.grids[0].rows * self.cell_size
        else:  # Single grid game
            width = self.game.grid.columns * self.cell_size
            height = self.game.grid.rows * self.cell_size

        self.canvas = tk.Canvas(
            self.root,
            width=width,
            height=height,
            bg='white'
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Create labels for controls
        if hasattr(self.game, 'controls'):
            controls1 = "Player 1: WASD + Space"
            controls2 = "Player 2: Arrows + Enter"
            tk.Label(self.root, text=controls1).pack()
            tk.Label(self.root, text=controls2).pack()

        self.root.bind('<Key>', self.game.handle_key_press)
        self.root.bind('<KeyRelease>', self.game.handle_key_release)

    def draw_grid(self) -> None:
        if not self.canvas:
            return

        self.canvas.delete('all')

        if hasattr(self.game, 'grids'):  # Multiplayer games
            # Draw both grids
            for player in range(len(self.game.grids)):
                offset_x = (self.game.grids[0].columns * self.cell_size + self.padding) * player
                
                # Draw grid background
                for row in range(self.game.grids[player].rows):
                    for col in range(self.game.grids[player].columns):
                        x1 = offset_x + col * self.cell_size
                        y1 = row * self.cell_size
                        x2 = x1 + self.cell_size
                        y2 = y1 + self.cell_size
                        
                        tile = self.game.grids[player].get_tile(row, col)
                        if tile:
                            # For Tetris tiles, use tile_type as color if tile_color is not present
                            color = getattr(tile, 'tile_color', tile.tile_type)
                            self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                       fill=color, outline='gray')
                        else:
                            self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                       fill='lightgray', outline='gray')

                # Draw current piece based on game type
                if self.game.current_pieces[player]:
                    piece = self.game.current_pieces[player]
                    
                    # Handle PuzzleFighter format
                    if hasattr(piece, 'get_positions') and len(piece.get_positions()[0]) == 3:
                        for x, y, tile in piece.get_positions():
                            if y >= 0:  # Only draw if visible
                                x1 = offset_x + x * self.cell_size
                                y1 = y * self.cell_size
                                x2 = x1 + self.cell_size
                                y2 = y1 + self.cell_size
                                self.canvas.create_rectangle(x1, y1, x2, y2,
                                                           fill=tile.tile_color,
                                                           outline='white')
                    # Handle Tetris format
                    else:
                        for x, y in piece.get_positions():
                            if y >= 0:  # Only draw if visible
                                x1 = offset_x + x * self.cell_size
                                y1 = y * self.cell_size
                                x2 = x1 + self.cell_size
                                y2 = y1 + self.cell_size
                                self.canvas.create_rectangle(x1, y1, x2, y2,
                                                           fill=piece.color,
                                                           outline='white')

                # Draw score
                self.canvas.create_text(
                    offset_x + 10, 10,
                    anchor='nw',
                    text=f'P{player+1} Score: {self.game.scores[player]}',
                    fill='black'
                )

                # Draw game over
                if self.game.game_over[player]:
                    self.canvas.create_text(
                        offset_x + (self.game.grids[player].columns * self.cell_size) // 2,
                        (self.game.grids[player].rows * self.cell_size) // 2,
                        text="GAME OVER",
                        fill='red',
                        font=('Arial', 20, 'bold')
                    )

        else:
            if not self.canvas:
                return

            self.canvas.delete('all')
            
            # Draw grid background
            for row in range(self.game.grid.rows):
                for col in range(self.game.grid.columns):
                    x1 = col * self.cell_size
                    y1 = row * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    
                    tile = self.game.grid.get_tile(row, col)
                    if tile:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=tile.tile_type, outline='gray')
                    else:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill='lightgray', outline='gray')

            # Draw current piece for Tetris
            if hasattr(self.game, 'current_piece') and self.game.current_piece:
                for x, y in self.game.current_piece.get_positions():
                    if y >= 0:  # Only draw if visible
                        x1 = x * self.cell_size
                        y1 = y * self.cell_size
                        x2 = x1 + self.cell_size
                        y2 = y1 + self.cell_size
                        self.canvas.create_rectangle(
                            x1, y1, x2, y2,
                            fill=self.game.current_piece.color,
                            outline='white'
                        )

            # Draw score if it's a Tetris game
            if hasattr(self.game, 'score'):
                self.canvas.create_text(
                    10, 10,
                    anchor='nw',
                    text=f'Score: {self.game.score}',
                    fill='black'
                )

    def _get_tile_color(self, tile: Tile) -> str:
        # Convert tile type to color - this is just an example
        colors = {
            0: 'red',
            1: 'blue',
            2: 'green',
            3: 'yellow',
            4: 'purple'
        }
        return colors.get(tile.tile_type, 'gray')

    def update(self) -> None:
        self.game.update()
        self.draw_grid()
        self.root.after(16, self.update)  # ~60 FPS
