import pygame
import time
import csv
import os
from datetime import datetime


class GameManager:
    def __init__(self):
        self.score = 0
        self.game_over = False
        self.game_completed = False
        self.death_count = 0
        self.start_time = pygame.time.get_ticks()
        self.completion_time = 0
        self.death_causes = {
            'falling': 0,
            'obstacle': 0,
            'left_behind': 0  # New death cause for player getting left behind by scrolling
        }
        self.session_id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.data_points = []
        self.last_data_collection = 0
        self.data_collection_interval = 10000  # 10 seconds in milliseconds

        # Ensure stats directory exists
        if not os.path.exists('stats'):
            os.makedirs('stats')

        # Create stats file if it doesn't exist
        if not os.path.exists('stats/game_stats.csv'):
            with open('stats/game_stats.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['session_id', 'timestamp', 'distance_traveled',
                                 'coins_collected', 'jump_count', 'score',
                                 'completion_time', 'death_cause'])

    def start_timer(self):
        """Start the game timer"""
        self.start_time = time.time()

    def end_timer(self):
        """End the game timer and calculate completion time"""
        if self.start_time:
            self.completion_time = time.time() - self.start_time
            return self.completion_time
        return 0

    def update_score(self, value):
        """Update the game score"""
        self.score += value

    def check_game_over(self, player, screen_height, obstacles=None):
        """Check if the game is over"""
        # Check if player fell off the screen
        if player.y > screen_height:
            self.game_over = True
            self.death_causes['falling'] += 1
            return True

        # Check for collision with obstacles if provided
        if obstacles:
            for obstacle in obstacles:
                if player.get_rect().colliderect(obstacle.get_rect()):
                    self.game_over = True
                    self.death_causes['obstacle'] += 1
                    return True

        return False

    def collect_data_point(self, player):
        """Collect a data point for statistics"""
        current_time = pygame.time.get_ticks()

        # Collect data at regular intervals or when requested
        if current_time - self.last_data_collection >= self.data_collection_interval:
            self.last_data_collection = current_time

            data_point = {
                'session_id': self.session_id,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'distance_traveled': player.get_distance(),
                'coins_collected': player.get_coins_collected(),
                'jump_count': player.get_jump_count(),
                'score': self.score,
                'completion_time': self.completion_time if self.game_completed else 0,
                'death_cause': ''
            }

            self.data_points.append(data_point)

    def save_game_stats(self, player):
        """Save game statistics to CSV file"""
        # Add final data point
        final_data = {
            'session_id': self.session_id,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'distance_traveled': player.get_distance(),
            'coins_collected': player.get_coins_collected(),
            'jump_count': player.get_jump_count(),
            'score': self.score,
            'completion_time': self.completion_time,
            'death_cause': next((cause for cause, count in self.death_causes.items()
                                 if count > 0), '')
        }

        # Write to CSV
        with open('stats/game_stats.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                final_data['session_id'],
                final_data['timestamp'],
                final_data['distance_traveled'],
                final_data['coins_collected'],
                final_data['jump_count'],
                final_data['score'],
                final_data['completion_time'],
                final_data['death_cause']
            ])

        # Also save intermediate data points
        for data_point in self.data_points:
            with open('stats/game_stats.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    data_point['session_id'],
                    data_point['timestamp'],
                    data_point['distance_traveled'],
                    data_point['coins_collected'],
                    data_point['jump_count'],
                    data_point['score'],
                    data_point['completion_time'],
                    data_point['death_cause']
                ])
