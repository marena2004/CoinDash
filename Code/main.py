import pygame
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from game_window import GameWindow
from stats_window import StatsWindow


class Main:
    def __init__(self):
        # Initialize pygame for the game
        pygame.init()

        # Create the main tkinter window for menu
        self.root = tk.Tk()
        self.root.title("CoinDash")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (500 / 2)
        y = (screen_height / 2) - (400 / 2)
        self.root.geometry(f"500x400+{int(x)}+{int(y)}")

        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), width=20)
        self.style.configure("TLabel", font=("Arial", 16), padding=10)
        self.style.configure("Title.TLabel", font=("Arial", 24, "bold"))

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create title label
        title_label = ttk.Label(self.main_frame, text="CoinDash", style="Title.TLabel")
        title_label.pack(pady=10)

        # Game description
        description = "Run, jump, collect coins and avoid obstacles in this endless runner!"
        desc_label = ttk.Label(self.main_frame, text=description, wraplength=400)
        desc_label.pack(pady=10)

        # Create buttons frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        # Create buttons
        start_button = ttk.Button(button_frame, text="Start Game", command=self.start_game)
        start_button.pack(pady=10)

        stats_button = ttk.Button(button_frame, text="Statistics", command=self.show_stats)
        stats_button.pack(pady=10)

        help_button = ttk.Button(button_frame, text="How to Play", command=self.show_help)
        help_button.pack(pady=10)

        quit_button = ttk.Button(button_frame, text="Quit", command=self.quit_game)
        quit_button.pack(pady=10)

        # Add quit button to the game window as well
        self.root.protocol("WM_DELETE_WINDOW", self.quit_game)

    def start_game(self):
        """Starts the game by closing the tkinter window and launching the pygame window"""
        try:
            self.root.withdraw()  # Hide main window instead of destroying it
            game_window = GameWindow()
            game_window.run()
            # After game ends, show the main menu again
            self.root.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while running the game: {str(e)}")
            self.root.deiconify()

    def show_stats(self):
        """Opens the statistics window"""
        try:
            self.root.withdraw()  # Hide main window
            stats_window = StatsWindow(self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while showing statistics: {str(e)}")
            self.root.deiconify()

    def show_help(self):
        """Shows help information"""
        help_window = tk.Toplevel(self.root)
        help_window.title("How to Play")
        help_window.geometry("500x400")
        help_window.transient(self.root)  # Set as transient to main window

        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (500 / 2)
        y = (screen_height / 2) - (400 / 2)
        help_window.geometry(f"500x400+{int(x)}+{int(y)}")

        # Add content
        help_frame = ttk.Frame(help_window, padding=20)
        help_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(help_frame, text="How to Play CoinDash", style="Title.TLabel").pack(pady=10)

        # Controls
        ttk.Label(help_frame, text="Controls:", font=("Arial", 14, "bold")).pack(anchor="w", pady=(20, 5))
        ttk.Label(help_frame, text="• Left/Right Arrow Keys: Move").pack(anchor="w", padx=20)
        ttk.Label(help_frame, text="• Space: Jump").pack(anchor="w", padx=20)
        ttk.Label(help_frame, text="• ESC: Pause/Resume").pack(anchor="w", padx=20)
        ttk.Label(help_frame, text="• R: Restart (after game over)").pack(anchor="w", padx=20)

        # Gameplay
        ttk.Label(help_frame, text="Gameplay:", font=("Arial", 14, "bold")).pack(anchor="w", pady=(20, 5))
        ttk.Label(help_frame, text="• The screen automatically scrolls right").pack(anchor="w", padx=20)
        ttk.Label(help_frame, text="• Jump from platform to platform").pack(anchor="w", padx=20)
        ttk.Label(help_frame, text="• Collect coins to increase your score").pack(anchor="w", padx=20)
        ttk.Label(help_frame, text="• Avoid obstacles (red blocks)").pack(anchor="w", padx=20)
        ttk.Label(help_frame, text="• Don't fall off the screen or get left behind!").pack(anchor="w", padx=20)

        # Close button
        ttk.Button(help_frame, text="Close", command=help_window.destroy).pack(pady=20)

    def quit_game(self):
        """Quits the application"""
        self.root.destroy()
        pygame.quit()
        sys.exit()

    def run(self):
        """Starts the tkinter main loop"""
        self.root.mainloop()


if __name__ == "__main__":
    main = Main()
    main.run()