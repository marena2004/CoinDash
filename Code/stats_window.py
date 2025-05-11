import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import numpy as np
from datetime import datetime


class StatsWindow:
    def __init__(self, root):
        self.parent = root

        try:
            # Create new top level window
            self.window = tk.Toplevel()
            self.window.title("Game Statistics")
            self.window.geometry("900x700")
            self.window.protocol("WM_DELETE_WINDOW", self.on_close)

            # Create notebook (tabbed interface)
            self.notebook = ttk.Notebook(self.window)
            self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

            # Create tabs
            self.overview_tab = ttk.Frame(self.notebook)
            self.sessions_tab = ttk.Frame(self.notebook)
            self.graphs_tab = ttk.Frame(self.notebook)
            self.detailed_graphs_tab = ttk.Frame(self.notebook)

            self.notebook.add(self.overview_tab, text="Overview")
            self.notebook.add(self.sessions_tab, text="Sessions")
            self.notebook.add(self.graphs_tab, text="Primary Graphs")
            self.notebook.add(self.detailed_graphs_tab, text="Additional Graphs")

            # Load data
            self.load_data()

            # Setup UI elements
            self.setup_overview_tab()
            self.setup_sessions_tab()
            self.setup_primary_graphs_tab()
            self.setup_detailed_graphs_tab()

            # Add quit button at the bottom of the window
            self.add_quit_button()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while showing statistics: {str(e)}")
            self.on_close()

    def add_quit_button(self):
        """Add a quit button at the bottom of the window"""
        quit_frame = ttk.Frame(self.window)
        quit_frame.pack(side="bottom", fill="x", padx=10, pady=5)

        quit_button = ttk.Button(
            quit_frame,
            text="Quit",
            command=self.on_close,
            style="Accent.TButton"  # Optional: Use a different style if available
        )
        quit_button.pack(side="right", padx=10, pady=5)

    def load_data(self):
        """Load game statistics data from CSV"""
        stats_file = 'stats/game_stats.csv'
        if os.path.exists(stats_file):
            try:
                self.stats_df = pd.read_csv(stats_file)
                # Convert timestamp to datetime
                self.stats_df['timestamp'] = pd.to_datetime(self.stats_df['timestamp'])

                # If no data or empty dataframe, create sample data for testing
                if self.stats_df.empty:
                    self.create_sample_data()
            except Exception as e:
                print(f"Error loading stats: {e}")
                self.create_sample_data()
        else:
            # Create directory if it doesn't exist
            os.makedirs('stats', exist_ok=True)
            self.create_sample_data()
            # Save sample data
            self.stats_df.to_csv(stats_file, index=False)
            print("Created sample stats file for testing.")

    def create_sample_data(self):
        """Create sample data for testing if no real data exists"""
        # Create sample timestamps for last 50 sessions
        now = datetime.now()
        timestamps = [now - pd.Timedelta(days=i) for i in range(50)]

        # Create sample data
        data = {
            'session_id': [f"session_{i + 1}" for i in range(50)],
            'timestamp': timestamps,
            'distance_traveled': np.random.uniform(100, 1000, 50),
            'coins_collected': np.random.randint(0, 50, 50),
            'jump_count': np.random.randint(10, 100, 50),
            'score': np.random.randint(100, 1000, 50),
            'completion_time': np.random.uniform(30, 300, 50),
            'death_cause': np.random.choice(['falling', 'obstacle', 'left_behind'], 50)
        }

        self.stats_df = pd.DataFrame(data)

    def setup_overview_tab(self):
        """Setup the overview tab with summary statistics"""
        # Create a frame with scrollbar for the overview tab
        overview_frame = ttk.Frame(self.overview_tab)
        overview_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(overview_frame)
        scrollbar = ttk.Scrollbar(overview_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Enable scrolling with mouse wheel
        self.bind_mousewheel_to_canvas(canvas)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Calculate summary statistics
        if not self.stats_df.empty:
            # Group by session_id to get unique sessions
            unique_sessions = self.stats_df.drop_duplicates(subset=['session_id'])

            total_sessions = len(unique_sessions)
            total_distance = self.stats_df['distance_traveled'].sum()
            avg_distance = self.stats_df['distance_traveled'].mean()
            total_coins = self.stats_df['coins_collected'].sum()
            avg_coins = self.stats_df['coins_collected'].mean()
            total_jumps = self.stats_df['jump_count'].sum()
            avg_jumps = self.stats_df['jump_count'].mean()
            avg_score = self.stats_df['score'].mean()
            max_score = self.stats_df['score'].max()

            # Time statistics
            min_time = self.stats_df['completion_time'].min()
            max_time = self.stats_df['completion_time'].max()
            avg_time = self.stats_df['completion_time'].mean()
            std_time = self.stats_df['completion_time'].std()

            # Count death causes
            death_causes = self.stats_df['death_cause'].value_counts()
            falling_deaths = death_causes.get('falling', 0)
            obstacle_deaths = death_causes.get('obstacle', 0)
            left_behind_deaths = death_causes.get('left_behind', 0)
        else:
            total_sessions = 0
            total_distance = 0
            avg_distance = 0
            total_coins = 0
            avg_coins = 0
            total_jumps = 0
            avg_jumps = 0
            avg_score = 0
            max_score = 0
            min_time = 0
            max_time = 0
            avg_time = 0
            std_time = 0
            falling_deaths = 0
            obstacle_deaths = 0
            left_behind_deaths = 0

        # Player Engagement Statistics
        engagement_frame = ttk.LabelFrame(scrollable_frame, text="Player Engagement Statistics")
        engagement_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(engagement_frame, text=f"Total Play Sessions: {total_sessions}", font=("Arial", 12)).pack(anchor="w",
                                                                                                            padx=10,
                                                                                                            pady=5)
        ttk.Label(engagement_frame, text=f"Total Distance Traveled: {total_distance:.1f} units",
                  font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        ttk.Label(engagement_frame, text=f"Average Distance per Session: {avg_distance:.1f} units",
                  font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        ttk.Label(engagement_frame, text=f"Total Jumps: {total_jumps}", font=("Arial", 12)).pack(anchor="w", padx=10,
                                                                                                 pady=5)
        ttk.Label(engagement_frame, text=f"Average Jumps per Session: {avg_jumps:.1f}", font=("Arial", 12)).pack(
            anchor="w", padx=10, pady=5)

        # Performance Statistics
        performance_frame = ttk.LabelFrame(scrollable_frame, text="Performance Statistics")
        performance_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(performance_frame, text=f"Total Coins Collected: {total_coins}", font=("Arial", 12)).pack(anchor="w",
                                                                                                            padx=10,
                                                                                                            pady=5)
        ttk.Label(performance_frame, text=f"Average Coins per Session: {avg_coins:.1f}", font=("Arial", 12)).pack(
            anchor="w", padx=10, pady=5)
        ttk.Label(performance_frame, text=f"Average Score: {avg_score:.1f}", font=("Arial", 12)).pack(anchor="w",
                                                                                                      padx=10, pady=5)
        ttk.Label(performance_frame, text=f"High Score: {max_score}", font=("Arial", 12)).pack(anchor="w", padx=10,
                                                                                               pady=5)

        # Time Statistics
        time_frame = ttk.LabelFrame(scrollable_frame, text="Completion Time Statistics")
        time_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(time_frame, text=f"Minimum Completion Time: {min_time:.1f} seconds", font=("Arial", 12)).pack(
            anchor="w", padx=10, pady=5)
        ttk.Label(time_frame, text=f"Maximum Completion Time: {max_time:.1f} seconds", font=("Arial", 12)).pack(
            anchor="w", padx=10, pady=5)
        ttk.Label(time_frame, text=f"Average Completion Time: {avg_time:.1f} seconds", font=("Arial", 12)).pack(
            anchor="w", padx=10, pady=5)
        ttk.Label(time_frame, text=f"Standard Deviation: {std_time:.1f} seconds", font=("Arial", 12)).pack(anchor="w",
                                                                                                           padx=10,
                                                                                                           pady=5)

        # Death statistics
        death_frame = ttk.LabelFrame(scrollable_frame, text="Death Statistics")
        death_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(death_frame,
                  text=f"Falling Deaths: {falling_deaths} ({falling_deaths / total_sessions * 100:.1f}% of sessions)",
                  font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        ttk.Label(death_frame,
                  text=f"Obstacle Collisions: {obstacle_deaths} ({obstacle_deaths / total_sessions * 100:.1f}% of sessions)",
                  font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        ttk.Label(death_frame,
                  text=f"Left Behind: {left_behind_deaths} ({left_behind_deaths / total_sessions * 100:.1f}% of sessions)",
                  font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

    def setup_sessions_tab(self):
        """Setup the sessions tab with detailed session data"""
        # Create treeview for sessions
        columns = ("session_id", "timestamp", "distance", "coins", "jumps", "score", "time", "death_cause")
        self.tree = ttk.Treeview(self.sessions_tab, columns=columns, show="headings")

        # Define column headings
        self.tree.heading("session_id", text="Session ID")
        self.tree.heading("timestamp", text="Date/Time")
        self.tree.heading("distance", text="Distance")
        self.tree.heading("coins", text="Coins")
        self.tree.heading("jumps", text="Jumps")
        self.tree.heading("score", text="Score")
        self.tree.heading("time", text="Time (s)")
        self.tree.heading("death_cause", text="Death Cause")

        # Set column widths
        self.tree.column("session_id", width=100)
        self.tree.column("timestamp", width=150)
        self.tree.column("distance", width=70)
        self.tree.column("coins", width=50)
        self.tree.column("jumps", width=50)
        self.tree.column("score", width=50)
        self.tree.column("time", width=70)
        self.tree.column("death_cause", width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.sessions_tab, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Controls frame for filtering and sorting
        controls_frame = ttk.Frame(self.sessions_tab)
        controls_frame.pack(side="bottom", fill="x", padx=10, pady=5)

        # Sort by options
        ttk.Label(controls_frame, text="Sort by:").pack(side="left", padx=5)
        sort_options = ["timestamp", "distance_traveled", "coins_collected", "jump_count", "score", "completion_time"]
        sort_display = ["timestamp", "distance", "coins", "jumps", "score", "time"]
        self.sort_var = tk.StringVar(value="timestamp")
        sort_dropdown = ttk.Combobox(controls_frame, textvariable=self.sort_var, values=sort_display, width=10,
                                     state="readonly")
        sort_dropdown.pack(side="left", padx=5)

        # Mapping for display names to actual column names
        self.sort_mapping = dict(zip(sort_display, sort_options))

        # Sort order
        self.sort_ascending = tk.BooleanVar(value=False)
        ttk.Checkbutton(controls_frame, text="Ascending", variable=self.sort_ascending).pack(side="left", padx=5)

        # Apply button
        ttk.Button(controls_frame, text="Apply Sort", command=self.populate_sessions_table).pack(side="left", padx=5)

        # Populate treeview with data
        self.populate_sessions_table()

    def populate_sessions_table(self):
        """Populate the sessions table with data"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add data from dataframe
        if not self.stats_df.empty:
            # Get sort options
            sort_display = self.sort_var.get()
            sort_col = self.sort_mapping.get(sort_display, "timestamp")  # Use mapping to get actual column name
            ascending = self.sort_ascending.get()

            # Group by session_id to get unique sessions
            unique_sessions = self.stats_df.drop_duplicates(subset=['session_id'])

            # Sort data (with error handling)
            try:
                unique_sessions = unique_sessions.sort_values(by=sort_col, ascending=ascending)
            except Exception as e:
                print(f"Error sorting by {sort_col}: {e}")
                # Fallback to timestamp sorting
                unique_sessions = unique_sessions.sort_values(by="timestamp", ascending=ascending)

            for _, row in unique_sessions.iterrows():
                # Format timestamp
                timestamp = row['timestamp'].strftime("%Y-%m-%d %H:%M")

                # Add row to treeview
                self.tree.insert("", "end", values=(
                    row['session_id'],
                    timestamp,
                    f"{row['distance_traveled']:.1f}",
                    row['coins_collected'],
                    row['jump_count'],
                    row['score'],
                    f"{row['completion_time']:.1f}",
                    row['death_cause']
                ))

    def bind_mousewheel_to_canvas(self, canvas):
        """Bind mousewheel to canvas for better scrolling"""
        # For Windows and MacOS
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

        # For Linux
        canvas.bind_all("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))

        # Track when this canvas is active for proper scrolling
        canvas.bind("<Enter>", lambda event: self.set_active_canvas(canvas))
        canvas.bind("<Leave>", lambda event: self.clear_active_canvas())

    def set_active_canvas(self, canvas):
        """Set the currently active canvas for scrolling"""
        self.active_canvas = canvas

    def clear_active_canvas(self):
        """Clear the active canvas reference"""
        if hasattr(self, 'active_canvas'):
            self.active_canvas = None

    def setup_primary_graphs_tab(self):
        """Setup the primary graphs tab with visualizations"""
        if self.stats_df.empty:
            ttk.Label(self.graphs_tab, text="No data available for graphs", font=("Arial", 12)).pack(pady=20)
            return

        # Create frame with scrollbar for the graphs tab
        graphs_frame = ttk.Frame(self.graphs_tab)
        graphs_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(graphs_frame)
        scrollbar = ttk.Scrollbar(graphs_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Enable scrolling with mousewheel
        self.bind_mousewheel_to_canvas(canvas)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 1. Line Graph: Player Movement (Distance Traveled) over time
        distance_frame = ttk.LabelFrame(scrollable_frame, text="Distance Traveled Over Time")
        distance_frame.pack(fill="both", expand=True, padx=10, pady=10)

        fig1, ax1 = plt.subplots(figsize=(8, 4))
        distance_data = self.stats_df.drop_duplicates(subset=['session_id']).sort_values('timestamp')
        ax1.plot(range(1, len(distance_data) + 1), distance_data['distance_traveled'], 'g-o', linewidth=2)
        ax1.set_title('Player Movement Over Time')
        ax1.set_xlabel('Session Number')
        ax1.set_ylabel('Distance Traveled')
        ax1.grid(True)

        canvas1 = FigureCanvasTkAgg(fig1, master=distance_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)

        # 2. Bar Chart: Coins Collected per session
        coins_frame = ttk.LabelFrame(scrollable_frame, text="Coins Collected per Session")
        coins_frame.pack(fill="both", expand=True, padx=10, pady=10)

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        coins_data = self.stats_df.drop_duplicates(subset=['session_id']).sort_values('timestamp').tail(
            15)  # Last 15 sessions
        bars = ax2.bar(range(1, len(coins_data) + 1), coins_data['coins_collected'], color='gold')
        ax2.set_title('Coins Collected (Last 15 Sessions)')
        ax2.set_xlabel('Session Number')
        ax2.set_ylabel('Coins Collected')
        ax2.set_xticks(range(1, len(coins_data) + 1))

        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                     f'{int(height)}', ha='center', va='bottom')

        canvas2 = FigureCanvasTkAgg(fig2, master=coins_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)

        # 3. Pie Chart: Death Causes
        death_frame = ttk.LabelFrame(scrollable_frame, text="Death Causes")
        death_frame.pack(fill="both", expand=True, padx=10, pady=10)

        fig3, ax3 = plt.subplots(figsize=(7, 5))
        death_counts = self.stats_df['death_cause'].value_counts()
        labels = death_counts.index
        sizes = death_counts.values
        explode = [0.1] * len(labels)  # explode all slices

        ax3.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90, colors=['tomato', 'orange', 'gold'])
        ax3.axis('equal')
        ax3.set_title('Death Causes Distribution')

        canvas3 = FigureCanvasTkAgg(fig3, master=death_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill="both", expand=True)

    def setup_detailed_graphs_tab(self):
        """Setup additional graphs tab with more visualizations"""
        if self.stats_df.empty:
            ttk.Label(self.detailed_graphs_tab, text="No data available for graphs", font=("Arial", 12)).pack(pady=20)
            return

        # Create frame with scrollbar for the detailed graphs tab
        detailed_frame = ttk.Frame(self.detailed_graphs_tab)
        detailed_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(detailed_frame)
        scrollbar = ttk.Scrollbar(detailed_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Enable scrolling with mousewheel
        self.bind_mousewheel_to_canvas(canvas)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 1. Scatter Plot: Jump Frequency
        jump_frame = ttk.LabelFrame(scrollable_frame, text="Jump Frequency Analysis")
        jump_frame.pack(fill="both", expand=True, padx=10, pady=10)

        fig1, ax1 = plt.subplots(figsize=(8, 4))
        jump_data = self.stats_df.drop_duplicates(subset=['session_id']).sort_values('timestamp')
        scatter = ax1.scatter(range(1, len(jump_data) + 1), jump_data['jump_count'],
                              c=jump_data['score'], cmap='viridis', alpha=0.7,
                              s=100, edgecolors='black', linewidth=1)
        ax1.set_title('Jump Frequency per Session')
        ax1.set_xlabel('Session Number')
        ax1.set_ylabel('Number of Jumps')
        ax1.grid(True, linestyle='--', alpha=0.7)

        # Add color bar to show score relationship
        cbar = plt.colorbar(scatter, ax=ax1)
        cbar.set_label('Score')

        canvas1 = FigureCanvasTkAgg(fig1, master=jump_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)

        # 2. Histogram: Completion Time
        time_frame = ttk.LabelFrame(scrollable_frame, text="Completion Time Distribution")
        time_frame.pack(fill="both", expand=True, padx=10, pady=10)

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        time_data = self.stats_df['completion_time']

        # Create histogram without density curve
        n, bins, patches = ax2.hist(time_data, bins=10, alpha=0.7, color='skyblue', edgecolor='black')

        # Add lines for mean and median
        mean_time = time_data.mean()
        median_time = time_data.median()
        ax2.axvline(mean_time, color='red', linestyle='--', linewidth=1.5, label=f'Mean: {mean_time:.1f}s')
        ax2.axvline(median_time, color='green', linestyle='-.', linewidth=1.5, label=f'Median: {median_time:.1f}s')

        ax2.set_title('Distribution of Completion Times')
        ax2.set_xlabel('Completion Time (seconds)')
        ax2.set_ylabel('Frequency')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()

        canvas2 = FigureCanvasTkAgg(fig2, master=time_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)

        # 3. Combined graph: Score vs. Distance & Coins
        combined_frame = ttk.LabelFrame(scrollable_frame, text="Performance Correlation Analysis")
        combined_frame.pack(fill="both", expand=True, padx=10, pady=10)

        fig3, ax3 = plt.subplots(figsize=(8, 5))

        # Primary scatter plot: Distance vs Score
        scatter1 = ax3.scatter(self.stats_df['distance_traveled'], self.stats_df['score'],
                               alpha=0.7, s=80, label='Score vs Distance', c='blue')
        ax3.set_xlabel('Distance Traveled')
        ax3.set_ylabel('Score', color='blue')
        ax3.tick_params(axis='y', labelcolor='blue')
        ax3.grid(True, linestyle='--', alpha=0.7)

        # Create second y-axis for coins
        ax4 = ax3.twinx()
        scatter2 = ax4.scatter(self.stats_df['distance_traveled'], self.stats_df['coins_collected'],
                               alpha=0.7, s=60, label='Coins vs Distance', c='green', marker='s')
        ax4.set_ylabel('Coins Collected', color='green')
        ax4.tick_params(axis='y', labelcolor='green')

        # Add title and legend
        fig3.suptitle('Score and Coins vs Distance Traveled')
        lines, labels = ax3.get_legend_handles_labels()
        lines2, labels2 = ax4.get_legend_handles_labels()
        ax3.legend(lines + lines2, labels + labels2, loc='upper left')

        fig3.tight_layout()
        canvas3 = FigureCanvasTkAgg(fig3, master=combined_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill="both", expand=True)

    def on_close(self):
        """Handle window close event"""
        try:
            plt.close('all')  # Close all matplotlib figures

            # Unbind all mouse wheel bindings
            try:
                self.window.unbind_all("<MouseWheel>")
                self.window.unbind_all("<Button-4>")
                self.window.unbind_all("<Button-5>")
            except:
                pass

            if hasattr(self, 'window') and self.window:
                self.window.destroy()
            if hasattr(self, 'parent') and self.parent:
                self.parent.deiconify()  # Show parent window
        except Exception as e:
            print(f"Error during window close: {e}")