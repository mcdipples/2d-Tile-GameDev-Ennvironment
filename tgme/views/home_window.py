import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Type
from tgme.player_profile import PlayerProfile
from tgme.player import Player
from tgme.tmge import TMGE
from tgme.views.game_ui import GameUI
from games.tetris_game import TetrisGame
from games.puzzle_fighter_game import PuzzleFighterGame

class HomeWindow:
    def __init__(self, tmge, profile, game_controls_dict) -> None:
        self.tmge = tmge
        self.profile = profile
        self.window = tk.Tk()
        self.window.title("TMGE Gaming Hub")
        self.window.geometry("1024x768")
        self.window.configure(bg='#ffffff')
        self.controls = controls
        
        # Configure styles
        self.style = ttk.Style()
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self) -> None:
        """Configure modern ttk styles"""
        self.style.configure('Modern.TFrame', background='#ffffff')
        self.style.configure('Card.TFrame', background='#f8f9fa')
        
        self.style.configure('Title.TLabel',
                            font=('Helvetica', 28, 'bold'),
                            background='#ffffff')
        
        self.style.configure('Header.TLabel',
                            font=('Helvetica', 20, 'bold'),
                            background='#f8f9fa')
        
        self.style.configure('Stats.TLabel',
                            font=('Helvetica', 12),
                            background='#f8f9fa')

    def create_widgets(self) -> None:
        self.create_menu()
        
        # Main container
        main_container = ttk.Frame(self.window, style='Modern.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Header with welcome message
        ttk.Label(
            main_container,
            text=f"Welcome back, {self.profile.username}",
            style='Title.TLabel'
        ).pack(anchor='w', pady=(0, 30))

        # Content container
        content = ttk.Frame(main_container, style='Modern.TFrame')
        content.pack(fill=tk.BOTH, expand=True)
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)

        # Games section
        self.create_games_section(content)
        
        # Stats section
        self.create_stats_section(content)

    def create_games_section(self, parent) -> None:
        games_frame = ttk.Frame(parent, style='Modern.TFrame')
        games_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 20))

        ttk.Label(
            games_frame,
            text="Available Games",
            style='Header.TLabel'
        ).pack(anchor='w', pady=(0, 20))

        # Games grid
        games_grid = ttk.Frame(games_frame, style='Modern.TFrame')
        games_grid.pack(fill=tk.BOTH, expand=True)

        for i, game in enumerate(self.tmge.get_available_games):
            game_card = self.create_game_card(games_grid, game)
            game_card.pack(fill=tk.X, pady=(0, 15))

    def create_game_card(self, parent, game) -> ttk.Frame:
        card = ttk.Frame(parent, style='Card.TFrame')
        card.configure(padding=20)

        # Game title
        ttk.Label(
            card,
            text=game.game_id,
            font=('Helvetica', 16, 'bold'),
            background='#f8f9fa'
        ).pack(side=tk.LEFT)

        # Play button
        play_btn = tk.Button(
            card,
            text="Play Now",
            command=lambda: self.start_game(game),
            bg='#007bff',
            fg='white',
            font=('Helvetica', 12),
            relief='flat',
            padx=20,
            pady=8
        )
        play_btn.pack(side=tk.RIGHT)

        return card

    def create_stats_section(self, parent) -> None:
        stats_frame = ttk.Frame(parent, style='Card.TFrame')
        stats_frame.grid(row=0, column=1, sticky='nsew')
        stats_frame.configure(padding=20)

        ttk.Label(
            stats_frame,
            text="Your Statistics",
            style='Header.TLabel'
        ).pack(anchor='w', pady=(0, 20))

        for game_id, stats in self.profile.stats.items():
            game_stats = ttk.Frame(stats_frame, style='Card.TFrame')
            game_stats.pack(fill=tk.X, pady=(0, 15))
            game_stats.configure(padding=15)

            ttk.Label(
                game_stats,
                text=game_id,
                font=('Helvetica', 14, 'bold'),
                background='#f8f9fa'
            ).pack(anchor='w', pady=(0, 10))

            for stat_name, value in stats.items():
                stat_text = f"{stat_name.replace('_', ' ').title()}: {value}"
                ttk.Label(
                    game_stats,
                    text=stat_text,
                    style='Stats.TLabel'
                ).pack(anchor='w', pady=2)

    def create_menu(self) -> None:
        """Create application menu bar"""
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Refresh Stats", command=self.refresh_stats)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_command(label="Exit", command=self.quit_application)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Game Controls", command=self.show_controls)
        help_menu.add_command(label="About", command=self.show_about)

    def start_game(self, game_template: Any) -> None:
        """Start a new instance of the selected game"""
        # Create a second player for multiplayer games
        player1 = Player(self.profile)
        player2 = Player(PlayerProfile("Player2"))

        # Create new instance of the game
        game_class = type(game_template)
        new_game = game_class(game_id=game_template.game_id, players=[player1, player2], controls=self.game_controls_dict[game_template.game_id])

        # Create new game window
        game_window = tk.Toplevel(self.window)
        game_window.title(f"Playing {new_game.game_id}")
        
        # Initialize game UI
        game_ui = GameUI(game_window, new_game)
        new_game.init()  # Initialize the new game instance
        game_ui.update()

    def refresh_stats(self) -> None:
        """Refresh player statistics"""
        # Implement stats refresh logic here
        messagebox.showinfo("Success", "Statistics refreshed!")

    def show_controls(self) -> None:
        """Show game controls help"""
        controls = {
            "Tetris": {
                "Player 1": "WASD + Space",
                "Player 2": "Arrow Keys + Enter"
            }
        }
        
        help_text = "Game Controls:\n\n"
        for game, players in controls.items():
            help_text += f"{game}:\n"
            for player, control in players.items():
                help_text += f"  {player}: {control}\n"
        
        messagebox.showinfo("Game Controls", help_text)

    def show_about(self) -> None:
        """Show about dialog"""
        about_text = """TMGE Gaming Hub
Version 1.0

A tile-matching game environment supporting
multiple games and local multiplayer.

© 2024 TMGE Team"""
        messagebox.showinfo("About TMGE", about_text)

    def logout(self) -> None:
        """Handle user logout"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.window.destroy()
            # Implement logout logic here

    def quit_application(self) -> None:
        """Handle application exit"""
        if messagebox.askyesno("Exit", "Are you sure you want to quit?"):
            self.tmge.quit()
            self.window.quit()
