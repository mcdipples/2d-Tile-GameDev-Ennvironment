import json
import os
from typing import List
from interfaces import IGameManager
from player_profile import PlayerProfile
from game import Game

class TMGE(IGameManager):
    def __init__(self) -> None:
        """
        __init__

        Args:
            None

        Returns:
            None
        """
        self.games: List[Game] = []
        self.player_profiles: List[PlayerProfile] = []
        self.profiles_file = "profiles.json"
        self.load_profiles()

    def load_profiles(self) -> None:
        """Load player profiles from file"""
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, 'r') as f:
                    profiles_data = json.load(f)
                    for profile_data in profiles_data:
                        profile = PlayerProfile(profile_data['username'])
                        profile.stats = profile_data.get('stats', {})
                        self.player_profiles.append(profile)
            except Exception as e:
                print(f"Error loading profiles: {e}")

    def save_profiles(self) -> None:
        """Save player profiles to file"""
        profiles_data = []
        for profile in self.player_profiles:
            profile_data = {
                'username': profile.username,
                'stats': profile.stats
            }
            profiles_data.append(profile_data)
        
        try:
            with open(self.profiles_file, 'w') as f:
                json.dump(profiles_data, f)
        except Exception as e:
            print(f"Error saving profiles: {e}")

    def register_game(self, game: Game) -> None:
        """
        register_game

        Args:
            game (Game): An instance of a concrete game to register with TMGE

        Returns:
            None
        """
        self.games.append(game)

    def get_available_games(self) -> List[Game]:
        """
        get_available_games

        Args:
            None

        Returns:
            games (List[Game]): The list of all registered games
        """
        return self.games

    def get_player_profiles(self) -> List[PlayerProfile]:
        """
        get_player_profiles

        Args:
            None

        Returns:
            profiles (List[PlayerProfile]): The list of all registered player profiles
        """
        return self.player_profiles

    def add_player_profile(self, profile: PlayerProfile) -> None:
        """
        add_player_profile

        Args:
            profile (PlayerProfile): A new player profile to add to TMGE

        Returns:
            None
        """
        self.player_profiles.append(profile)
        self.save_profiles()

    def start(self) -> None:
        """
        start

        Args:
            None

        Returns:
            None
        """
        print("TMGE started.")

    def quit(self) -> None:
        """
        quit

        Args:
            None

        Returns:
            None
        """
        self.save_profiles()
        print("TMGE quit.")