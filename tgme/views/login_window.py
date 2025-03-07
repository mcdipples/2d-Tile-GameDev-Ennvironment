import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from tgme.player_profile import PlayerProfile
from tgme.tmge import TMGE

class LoginWindow:
    def __init__(self, tmge: TMGE, on_login_success) -> None:
        self.tmge = tmge
        self.on_login_success = on_login_success
        self.window = tk.Tk()
        self.window.title("TMGE Login")
        self.window.geometry("400x500")
        self.window.configure(bg='#ffffff')
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('Modern.TFrame', background='#ffffff')
        self.style.configure('Modern.TLabel', background='#ffffff', font=('Helvetica', 12))
        self.style.configure('Title.TLabel', background='#ffffff', font=('Helvetica', 24, 'bold'))
        self.style.configure('Modern.TButton', 
                           font=('Helvetica', 12),
                           padding=10,
                           background='#007bff')
        
        self.setup_ui()
        self.window.mainloop()

    def setup_ui(self) -> None:
        # Main container
        main_frame = ttk.Frame(self.window, style='Modern.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Logo/Title
        ttk.Label(
            main_frame,
            text="TMGE",
            style='Title.TLabel'
        ).pack(pady=(0, 30))

        # Username container
        username_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        username_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(
            username_frame,
            text="Username",
            style='Modern.TLabel'
        ).pack(anchor='w')

        self.username_entry = ttk.Entry(
            username_frame,
            font=('Helvetica', 12),
            width=30
        )
        self.username_entry.pack(fill=tk.X, pady=(5, 0))

        # Buttons container
        buttons_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        buttons_frame.pack(fill=tk.X, pady=(20, 0))

        login_btn = tk.Button(
            buttons_frame,
            text="Login",
            command=self.login,
            bg='#007bff',
            fg='white',
            font=('Helvetica', 12),
            relief='flat',
            padx=20,
            pady=10
        )
        login_btn.pack(fill=tk.X, pady=(0, 10))

        create_btn = tk.Button(
            buttons_frame,
            text="Create New Profile",
            command=self.show_create_profile,
            bg='#6c757d',
            fg='white',
            font=('Helvetica', 12),
            relief='flat',
            padx=20,
            pady=10
        )
        create_btn.pack(fill=tk.X)

    def login(self) -> None:
        username = self.username_entry.get()
        profiles = self.tmge.get_player_profiles
        
        for profile in profiles:
            if profile.username == username:
                self.window.destroy()
                self.on_login_success(profile)
                return

        messagebox.showerror("Error", "Profile not found!")

    def show_create_profile(self) -> None:
        create_window = tk.Toplevel(self.window)
        create_window.title("Create Profile")
        create_window.geometry("300x250")
        create_window.configure(bg='#ffffff')
        create_window.transient(self.window)
        create_window.grab_set()

        container = ttk.Frame(create_window, style='Modern.TFrame')
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        ttk.Label(
            container,
            text="Create New Profile",
            style='Title.TLabel'
        ).pack(pady=(0, 20))

        ttk.Label(
            container,
            text="Username",
            style='Modern.TLabel'
        ).pack(anchor='w')

        new_username_entry = ttk.Entry(
            container,
            font=('Helvetica', 12),
            width=25
        )
        new_username_entry.pack(fill=tk.X, pady=(5, 20))

        # Create profile button
        create_btn = tk.Button(
            container,
            text="Create Profile",
            command=lambda: self.create_profile(new_username_entry.get(), create_window),
            bg='#28a745',
            fg='white',
            font=('Helvetica', 12),
            relief='flat',
            padx=20,
            pady=10
        )
        create_btn.pack(fill=tk.X)

    def create_profile(self, new_username: str, create_window: tk.Toplevel) -> None:
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
