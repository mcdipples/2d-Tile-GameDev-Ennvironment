import tkinter as tk
from tkinter import messagebox
from player_profile import PlayerProfile
from tmge import TMGE

class LoginWindow:
    def __init__(self, tmge: TMGE, on_login_success) -> None:
        self.tmge = tmge
        self.on_login_success = on_login_success
        self.window = tk.Tk()
        self.window.title("TMGE Login")
        self.setup_ui()

    def setup_ui(self) -> None:
        # Username
        tk.Label(self.window, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack(pady=5)

        # Login button
        tk.Button(self.window, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.window, text="Create New Profile", command=self.show_create_profile).pack(pady=5)

    def login(self) -> None:
        username = self.username_entry.get()
        profiles = self.tmge.get_player_profiles()
        
        for profile in profiles:
            if profile.username == username:
                self.window.destroy()
                self.on_login_success(profile)
                return

        messagebox.showerror("Error", "Profile not found!")

    def show_create_profile(self) -> None:
        create_window = tk.Toplevel(self.window)
        create_window.title("Create Profile")

        tk.Label(create_window, text="New Username:").pack(pady=5)
        new_username_entry = tk.Entry(create_window)
        new_username_entry.pack(pady=5)

        def create_profile():
            new_username = new_username_entry.get()
            if not new_username:
                messagebox.showerror("Error", "Username cannot be empty!")
                return

            # Check if username already exists
            if any(p.username == new_username for p in self.tmge.get_player_profiles()):
                messagebox.showerror("Error", "Username already exists!")
                return

            profile = PlayerProfile(new_username)
            self.tmge.add_player_profile(profile)
            create_window.destroy()
            messagebox.showinfo("Success", "Profile created! You can now log in.")

        tk.Button(create_window, text="Create", command=create_profile).pack(pady=10)
