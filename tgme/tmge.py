import json
import os
from typing import List
from tgme.interfaces import IGameManager
from tgme.player_profile import PlayerProfile
from tgme.game import Game
from tgme.utils.logger import TMGELogger

class TMGE(IGameManager):
    def __init__(self) -> None:
        """
        __init__

        Args:
            None

        Returns:
            None
        """
        self.logger = TMGELogger()
        self.logger.info("Initializing TMGE")
        
        self.games: List[Game] = []
        self.player_profiles: List[PlayerProfile] = []
        
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(data_dir, exist_ok=True)
        
        self.profiles_file = os.path.join(data_dir, "profiles.json")
        self.load_profiles()

    def load_profiles(self) -> None:
        """Load player profiles from file"""
        self.logger.debug("Loading player profiles")
        if not os.path.exists(self.profiles_file):
            self.logger.info("Profiles file not found, creating new one")
            # Create empty profiles file if it doesn't exist
            try:
                with open(self.profiles_file, 'w') as f:
                    json.dump([], f)
            except Exception as e:
                print(f"Error creating profiles file: {e}")
            return

        try:
            with open(self.profiles_file, 'r') as f:
                profiles_data = json.load(f)
                for profile_data in profiles_data:
                    if isinstance(profile_data, dict) and 'username' in profile_data:
                        profile = PlayerProfile(profile_data['username'])
                        profile.stats = profile_data.get('stats', {})
                        self.player_profiles.append(profile)
        except json.JSONDecodeError:
            print("Error: profiles.json is corrupted. Creating new file.")
            with open(self.profiles_file, 'w') as f:
                json.dump([], f)
        except Exception as e:
            print(f"Error loading profiles: {e}")

    def save_profiles(self) -> None:
        """Save player profiles to file"""
        self.logger.debug("Saving player profiles")
        try:
            # Create backup of existing file
            if os.path.exists(self.profiles_file):
                backup_file = f"{self.profiles_file}.bak"
                try:
                    os.replace(self.profiles_file, backup_file)
                except Exception as e:
                    print(f"Error creating backup: {e}")

            profiles_data = []
            for profile in self.player_profiles:
                if hasattr(profile, 'username'):  # Validate profile object
                    profile_data = {
                        'username': profile.username,
                        'stats': getattr(profile, 'stats', {})
                    }
                    profiles_data.append(profile_data)

            # Write to temporary file first
            temp_file = f"{self.profiles_file}.tmp"
            with open(temp_file, 'w') as f:
                json.dump(profiles_data, f, indent=2)

            # Replace original file with temporary file
            os.replace(temp_file, self.profiles_file)
            self.logger.info("Profiles saved successfully")

        except Exception as e:
            self.logger.error(f"Failed to save profiles: {e}")
            print(f"Error saving profiles: {e}")
            # Try to restore from backup
            if os.path.exists(backup_file):
                try:
                    os.replace(backup_file, self.profiles_file)
                    print("Restored profiles from backup.")
                except Exception as restore_error:
                    print(f"Error restoring backup: {restore_error}")

    def register_game(self, game: Game) -> None:
        """
        register_game

        Args:
            game (Game): An instance of a concrete game to register with TMGE

        Returns:
            None
        """
        self.logger.info(f"Registering game: {game.game_id}")
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
        self.logger.info(f"Adding new player profile: {profile.username}")
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