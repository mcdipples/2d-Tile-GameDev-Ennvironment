import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any
from player_profile import PlayerProfile
from tmge import TMGE
from game_ui import GameUI

class HomeWindow:
    def __init__(self, tmge: TMGE, profile: PlayerProfile) -> None:
        self.tmge = tmge
        self.profile = profile
        self.window = tk.Tk()
        self.window.title("TMGE Gaming Hub")
        self.window.geometry("800x600")
        self.window.minsize(800, 600)
        self.create_widgets()
        self.style = ttk.Style()
        self.setup_styles()

    def setup_styles(self) -> None:
        """Configure ttk styles for widgets"""
        self.style.configure('Header.TLabel', font=('Helvetica', 24, 'bold'))
        self.style.configure('Subheader.TLabel', font=('Helvetica', 16))
        self.style.configure('GameButton.TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('Stats.TLabel', font=('Helvetica', 12))

    def create_widgets(self) -> None:
        """Create and arrange all GUI elements"""
        self.create_menu()
        
        # Main container
        main_container = ttk.Frame(self.window, padding="10")
        main_container.grid(row=0, column=0, sticky="nsew")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        ttk.Label(
            header_frame, 
            text=f"Welcome, {self.profile.username}!", 
            style='Header.TLabel'
        ).pack(pady=10)

        # Left panel - Game Selection
        games_frame = ttk.LabelFrame(main_container, text="Available Games", padding="10")
        games_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.create_games_panel(games_frame)

        # Right panel - Player Stats
        stats_frame = ttk.LabelFrame(main_container, text="Player Statistics", padding="10")
        stats_frame.grid(row=1, column=1, sticky="nsew")
        self.create_stats_panel(stats_frame)

        # Configure grid weights
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(1, weight=1)

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

    def create_games_panel(self, parent: ttk.Frame) -> None:
        """Create the games selection panel"""
        ttk.Label(
            parent,
            text="Select a game to play:",
            style='Subheader.TLabel'
        ).pack(pady=(0, 10))

        games_container = ttk.Frame(parent)
        games_container.pack(fill=tk.BOTH, expand=True)

        for game in self.tmge.get_available_games():
            game_frame = ttk.Frame(games_container, padding="5")
            game_frame.pack(fill=tk.X, pady=5)

            ttk.Label(
                game_frame,
                text=game.game_id,
                style='Stats.TLabel'
            ).pack(side=tk.LEFT)

            ttk.Button(
                game_frame,
                text="Play",
                style='GameButton.TButton',
                command=lambda g=game: self.start_game(g)
            ).pack(side=tk.RIGHT)

    def create_stats_panel(self, parent: ttk.Frame) -> None:
        """Create the player statistics panel"""
        ttk.Label(
            parent,
            text="Your Gaming Statistics",
            style='Subheader.TLabel'
        ).pack(pady=(0, 10))

        stats_container = ttk.Frame(parent)
        stats_container.pack(fill=tk.BOTH, expand=True)

        # Display stats for each game
        for game_id, stats in self.profile.stats.items():
            game_stats_frame = ttk.LabelFrame(
                stats_container,
                text=game_id,
                padding="5"
            )
            game_stats_frame.pack(fill=tk.X, pady=5)

            for stat_name, value in stats.items():
                ttk.Label(
                    game_stats_frame,
                    text=f"{stat_name.replace('_', ' ').title()}: {value}",
                    style='Stats.TLabel'
                ).pack(anchor='w')

    def start_game(self, game: Any) -> None:
        """Start the selected game"""
        game.init()
        game_window = tk.Toplevel(self.window)
        game_window.title(f"Playing {game.game_id}")
        game_ui = GameUI(game_window, game)
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
