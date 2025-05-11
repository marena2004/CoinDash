import pygame
import sys
import random
from player import Player
from platform_obj import Platform
from coin import Coin
from obstacle import Obstacle
from game_manager import GameManager
import math


class GameWindow:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Game window settings
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("CoinDash")

        # Try to load background image, use fallback if not found
        try:
            self.background_image = pygame.image.load("background.jpg").convert()
            self.background_image = pygame.transform.scale(self.background_image,
                                                           (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        except pygame.error:
            self.background_image = None
            print("Warning: background.jpg not found. Using solid color instead.")

        # Clock for controlling game speed
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Track active moving obstacles
        self.moving_obstacles = []

        # Game objects
        self.init_game_objects()

        # Game manager
        self.game_manager = GameManager()

        # Font for UI
        self.font = pygame.font.SysFont('Arial', 24)

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.BACKGROUND_COLOR = (135, 206, 235)  # Sky blue as fallback

        # Game state
        self.running = True
        self.paused = False

        # Camera and scrolling settings
        self.camera_offset_x = 0
        self.scroll_speed = 3  # Base scrolling speed
        self.distance_traveled = 0  # Distance in pixels
        self.distance_in_meters = 0  # Distance converted to meters (for display)
        self.pixels_per_meter = 30  # Conversion rate: 30 pixels = 1 meter

        # Platform generation
        self.last_platform_x = 800  # Start generating after initial platforms
        self.platform_gap_min = 80  # Reduced minimum gap for tighter platforms
        self.platform_gap_max = 200  # Reduced maximum gap for more achievable jumps

        # Coin and obstacle generation rates (higher = more frequent)
        self.coin_chance = 0.6  # 60% chance per platform (increased from 30%)
        self.obstacle_chance = 0.4  # 40% chance per platform (increased from 20%)

        # Coin patterns
        self.coin_patterns = [
            "single",  # Single coin
            "line",  # Horizontal line of coins
            "arc",  # Arc of coins
            "zigzag",  # Zigzag pattern
            "vertical",  # Vertical line of coins
        ]

        # Obstacle variety
        self.obstacle_types = [
            "standard",  # Standard obstacle
            "tall",  # Tall thin obstacle
            "wide",  # Wide short obstacle
            "moving",  # Moving obstacle
        ]

        # Add a starting grace period before scrolling begins
        self.start_delay = 60  # 60 frames = 1 second at 60 FPS
        self.current_delay = self.start_delay

        # Combo system for coin collection
        self.combo_counter = 0
        self.combo_timer = 0
        self.combo_timeout = 120  # 2 seconds at 60 FPS

        # Special effects
        self.particles = []

    def init_game_objects(self):
        """Initialize all game objects"""
        # Create initial platforms (these will be the starting area)
        self.platforms = [
            Platform(0, 555, 1000, 20),  # Starting platform (shortened to force generation)
            Platform(0, 500, 300, 20),  # Starting platform
            Platform(350, 500, 150, 20),  # Connected platform
            Platform(550, 500, 200, 20),  # Another connected platform
            Platform(800, 480, 150, 20),  # First jump platform
            Platform(1050, 450, 200, 20),  # Second platform
            Platform(1350, 480, 180, 20),  # Third platform
        ]

        # Create player directly on top of the first platform
        start_platform = self.platforms[0]
        player_x = 100
        # Position player exactly on top of platform (critical to position correctly)
        player_y = start_platform.y - 50  # Player height is 50
        self.player = Player(player_x, player_y)

        # Make sure player is positioned exactly on the platform
        self.player.on_ground = True  # Set initially to true
        self.player.velocity_y = 0  # No vertical movement at start

        # Set initial small velocity to help player move
        self.player.velocity_x = 2  # Give a small initial push

        # Run one physics update to properly set ground state and position
        self.player.move(self.platforms)

        # Initialize empty lists for coins and obstacles
        self.coins = []
        self.obstacles = []

        # Add initial coins in a more interesting pattern
        self.add_coin_pattern(200, 450, "line", 5)  # Line of 5 coins starting at x=200
        self.add_coin_pattern(400, 450, "arc", 5)  # Arc of 5 coins starting at x=400
        self.add_coin_pattern(650, 430, "zigzag", 5)  # Zigzag pattern starting at x=650
        self.add_coin_pattern(900, 410, "vertical", 3)  # Vertical line starting at x=900
        self.add_coin_pattern(1200, 400, "line", 3)  # Another line at x=1200

        # Add initial obstacles with variety
        self.obstacles = [
            Obstacle(950, 460, 40, 20),  # Standard obstacle
            Obstacle(1250, 430, 60, 10),  # Wide, short obstacle
            self.create_moving_obstacle(1100, 400, 30, 30, 1100, 1200)  # Moving obstacle
        ]

    def create_moving_obstacle(self, x, y, width, height, min_x, max_x, speed=1):
        """Create a moving obstacle and track it"""
        obstacle = Obstacle(x, y, width, height)
        # Add movement properties to the obstacle
        obstacle.min_x = min_x
        obstacle.max_x = max_x
        obstacle.speed = speed * random.choice([-1, 1])
        obstacle.is_moving = True

        # Add to moving obstacles list
        self.moving_obstacles.append(obstacle)
        return obstacle

    def add_coin_pattern(self, start_x, start_y, pattern_type, count):
        """Add a pattern of coins starting at the given position"""
        if pattern_type == "single":
            self.coins.append(Coin(start_x, start_y))

        elif pattern_type == "line":
            # Horizontal line of coins
            for i in range(count):
                self.coins.append(Coin(start_x + i * 30, start_y))

        elif pattern_type == "arc":
            # Arc of coins (half circle)
            radius = 50
            for i in range(count):
                angle = 3.14 * i / (count - 1)  # From 0 to pi
                x = start_x + i * 30
                y = start_y - int(radius * abs(math.sin(angle)))
                self.coins.append(Coin(x, y))

        elif pattern_type == "zigzag":
            # Zigzag pattern
            for i in range(count):
                y_offset = 20 if i % 2 == 0 else -20
                self.coins.append(Coin(start_x + i * 30, start_y + y_offset))

        elif pattern_type == "vertical":
            # Vertical line of coins
            for i in range(count):
                self.coins.append(Coin(start_x, start_y - i * 30))

    def generate_obstacles(self):
        """Generate obstacles independently to ensure consistent distribution"""
        # Check how many obstacles are visible on screen
        visible_obstacles = sum(1 for ob in self.obstacles if
                                -50 < ob.x - self.camera_offset_x < self.SCREEN_WIDTH + 100)

        # If we have fewer than 3-5 obstacles visible, generate more
        if visible_obstacles < 3:
            # Generate obstacles ahead of the player
            ahead_position = self.camera_offset_x + self.SCREEN_WIDTH * 1.2

            # Try to place on existing platforms
            potential_platforms = [p for p in self.platforms if
                                   p.x > ahead_position and
                                   p.x < ahead_position + self.SCREEN_WIDTH and
                                   p.width > 80]  # Only on platforms wide enough

            if potential_platforms:
                # Select a random platform
                platform = random.choice(potential_platforms)

                # Determine obstacle type
                obstacle_type = random.choice(["standard", "tall", "wide", "moving"])

                if obstacle_type == "standard":
                    obstacle_x = platform.x + random.randint(10, platform.width - 30)
                    obstacle_y = platform.y - 20
                    self.obstacles.append(Obstacle(obstacle_x, obstacle_y, 30, 20))

                elif obstacle_type == "tall":
                    obstacle_x = platform.x + random.randint(10, platform.width - 20)
                    obstacle_y = platform.y - 40
                    self.obstacles.append(Obstacle(obstacle_x, obstacle_y, 20, 40))

                elif obstacle_type == "wide":
                    obstacle_x = platform.x + random.randint(10, platform.width - 60)
                    obstacle_y = platform.y - 15
                    self.obstacles.append(Obstacle(obstacle_x, obstacle_y, 60, 15))

                elif obstacle_type == "moving" and platform.width > 150:
                    # Only create moving obstacles on wider platforms
                    obstacle_x = platform.x + random.randint(30, platform.width - 60)
                    obstacle_y = platform.y - 25
                    # Moving range is within platform boundaries
                    min_x = platform.x + 20
                    max_x = platform.x + platform.width - 40
                    self.create_moving_obstacle(obstacle_x, obstacle_y, 30, 25, min_x, max_x)
    def generate_new_elements(self):
        """Generate new platforms, coins, and obstacles as the player progresses"""
        last_floor_x = 0
        for platform in self.platforms:
            # Find the rightmost floor platform (platforms at y=555)
            if platform.y == 555 and platform.x + platform.width > last_floor_x:
                last_floor_x = platform.x + platform.width

        # Generate new floor segments if needed
        if last_floor_x - self.camera_offset_x < self.SCREEN_WIDTH * 2:
            # Decide if we want a gap in the floor
            if random.random() < 0.3:  # 30% chance for a gap
                gap_width = random.randint(100, 200)  # Gap size
                new_floor_x = last_floor_x + gap_width
                floor_width = random.randint(300, 600)  # Floor segment width
            else:
                new_floor_x = last_floor_x
                floor_width = random.randint(400, 800)  # Floor segment width

            # Create new floor segment
            new_floor = Platform(new_floor_x, 555, floor_width, 20)
            self.platforms.append(new_floor)

            if floor_width > 300 and random.random() < 0.4:  # 40% chance
                for _ in range(random.randint(1, 3)):  # 1-3 obstacles
                    obstacle_x = new_floor_x + random.randint(50, floor_width - 50)
                    obstacle_y = new_floor.y - 20
                    # Choose random obstacle type
                    obstacle_type = random.choice(["standard", "wide", "tall"])

                    if obstacle_type == "standard":
                        self.obstacles.append(Obstacle(obstacle_x, obstacle_y, 30, 20))
                    elif obstacle_type == "wide":
                        self.obstacles.append(Obstacle(obstacle_x, obstacle_y, 60, 15))
                    elif obstacle_type == "tall":
                        self.obstacles.append(Obstacle(obstacle_x, obstacle_y - 20, 20, 40))


            # Add some coins above the gaps
            if new_floor_x > last_floor_x:  # If there's a gap
                gap_center = last_floor_x + (new_floor_x - last_floor_x) / 2
                self.add_coin_pattern(gap_center - 50, 450, "arc", 5)

        # Check if we need to generate new platforms
        if self.last_platform_x - self.camera_offset_x < self.SCREEN_WIDTH * 1.5:
            # Generate new platform
            last_platform = self.platforms[-1]

            # Random gap between platforms
            gap = random.randint(self.platform_gap_min, self.platform_gap_max)

            # Calculate new platform position
            new_x = self.last_platform_x + gap

            # Vary the height slightly (within playable range)
            height_variance = random.randint(-30, 30)
            new_y = last_platform.y + height_variance
            new_y = max(300, min(500, new_y))  # Keep platforms in reasonable height range

            # Add some variety to platform size
            width = random.randint(100, 300)  # Increased max width for more variety
            height = 20  # Platform height

            # Occasionally create a floating platform above
            if random.random() < 0.25:  # 25% chance for a floating platform
                float_x = new_x + random.randint(20, width - 50)
                float_y = new_y - random.randint(80, 120)
                float_width = random.randint(80, 150)
                float_platform = Platform(float_x, float_y, float_width, height)
                self.platforms.append(float_platform)

                # Add coins to floating platform (higher value)
                if random.random() < 0.8:  # 80% chance for coins on floating platforms
                    pattern = random.choice(self.coin_patterns)
                    coin_count = random.randint(3, 6)
                    self.add_coin_pattern(float_x + 10, float_y - 30, pattern, coin_count)

            # Add new main platform
            new_platform = Platform(new_x, new_y, width, height)
            self.platforms.append(new_platform)

            # Update last platform x position
            self.last_platform_x = new_x + width

            # Add coins on the platform with higher chance
            if random.random() < self.coin_chance:
                pattern = random.choice(self.coin_patterns)
                coin_count = random.randint(3, 8)  # More coins in a group
                self.add_coin_pattern(new_x + random.randint(10, width - 10), new_y - 30, pattern, coin_count)

            # Add obstacle on the platform with higher chance
            if random.random() < self.obstacle_chance:
                obstacle_type = random.choice(self.obstacle_types)

                if obstacle_type == "standard":
                    obstacle_x = new_x + random.randint(10, width - 30)
                    obstacle_y = new_y - 20
                    self.obstacles.append(Obstacle(obstacle_x, obstacle_y, 30, 20))

                elif obstacle_type == "tall":
                    obstacle_x = new_x + random.randint(10, width - 20)
                    obstacle_y = new_y - 40
                    self.obstacles.append(Obstacle(obstacle_x, obstacle_y, 20, 40))

                elif obstacle_type == "wide":
                    obstacle_x = new_x + random.randint(10, width - 60)
                    obstacle_y = new_y - 15
                    self.obstacles.append(Obstacle(obstacle_x, obstacle_y, 60, 15))

                elif obstacle_type == "moving" and width > 150:
                    # Only create moving obstacles on wider platforms
                    obstacle_x = new_x + random.randint(30, width - 60)
                    obstacle_y = new_y - 25
                    # Moving range is within platform boundaries
                    min_x = new_x + 20
                    max_x = new_x + width - 40
                    self.create_moving_obstacle(obstacle_x, obstacle_y, 30, 25, min_x, max_x)

        # Remove platforms that are far behind (optimization)
        while self.platforms and self.platforms[0].x + self.platforms[0].width < self.camera_offset_x - 800:
            self.platforms.pop(0)

        # Remove coins that are far behind
        for i in range(len(self.coins) - 1, -1, -1):
            if self.coins[i].x < self.camera_offset_x - 800:
                self.coins.pop(i)

        # Remove obstacles that are far behind
        for i in range(len(self.obstacles) - 1, -1, -1):
            if self.obstacles[i].x < self.camera_offset_x - 800:
                # Also remove from moving obstacles list if applicable
                if hasattr(self.obstacles[i], 'is_moving'):
                    if self.obstacles[i] in self.moving_obstacles:
                        self.moving_obstacles.remove(self.obstacles[i])
                self.obstacles.pop(i)

    def update_moving_obstacles(self):
        """Update the position of moving obstacles"""
        for obstacle in self.moving_obstacles:
            # Move the obstacle
            obstacle.x += obstacle.speed

            # Reverse direction if reached boundary
            if obstacle.x <= obstacle.min_x or obstacle.x >= obstacle.max_x:
                obstacle.speed *= -1

    def create_coin_collect_particles(self, x, y):
        """Create particle effects when collecting coins"""
        for _ in range(8):  # Create 8 particles
            # Random velocity
            vel_x = random.uniform(-2, 2)
            vel_y = random.uniform(-4, -1)
            # Create particle (position, velocity, color, lifetime)
            particle = {
                'x': x, 'y': y,
                'vel_x': vel_x, 'vel_y': vel_y,
                'color': (255, 215, 0),  # Gold color
                'radius': random.uniform(1, 3),
                'lifetime': random.randint(15, 30)  # Frames
            }
            self.particles.append(particle)

    def update_particles(self):
        """Update particle effects"""
        for i in range(len(self.particles) - 1, -1, -1):
            # Update position
            self.particles[i]['x'] += self.particles[i]['vel_x']
            self.particles[i]['y'] += self.particles[i]['vel_y']

            # Apply gravity
            self.particles[i]['vel_y'] += 0.1

            # Decrease lifetime
            self.particles[i]['lifetime'] -= 1

            # Remove if expired
            if self.particles[i]['lifetime'] <= 0:
                self.particles.pop(i)

    def handle_events(self):
        """Handle player input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                # Save game stats before exiting
                if hasattr(self, 'game_manager'):
                    self.game_manager.save_game_stats(self.player)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                if event.key == pygame.K_SPACE and not self.paused:
                    self.player.jump()
                # Debug: Allow restart with 'R' key
                if event.key == pygame.K_r and self.game_manager.game_over:
                    self.reset_game()
                # Add quit key (Q)
                if event.key == pygame.K_q:
                    self.running = False
                    # Save game stats before exiting
                    if hasattr(self, 'game_manager'):
                        self.game_manager.save_game_stats(self.player)
                    pygame.quit()
                    sys.exit()

    def reset_game(self):
        """Reset the game after game over"""
        self.init_game_objects()
        self.camera_offset_x = 0
        self.distance_traveled = 0
        self.distance_in_meters = 0
        self.last_platform_x = 800
        self.scroll_speed = 3
        self.game_manager = GameManager()
        self.game_manager.start_timer()
        # Reset the starting delay
        self.current_delay = self.start_delay
        # Reset combo system
        self.combo_counter = 0
        self.combo_timer = 0
        # Clear particles
        self.particles = []
        # Clear moving obstacles
        self.moving_obstacles = []

    def update(self):
        """Update game state"""
        if self.paused or self.game_manager.game_over or self.game_manager.game_completed:
            return

        # Update start delay before scrolling begins
        if self.current_delay > 0:
            self.current_delay -= 1
            # During this grace period, still allow player to move but don't start scrolling
            self.player.move(self.platforms)
        else:
            # Update camera position (auto-scrolling) after delay
            self.camera_offset_x += self.scroll_speed
            self.distance_traveled = self.camera_offset_x
            self.distance_in_meters = self.distance_traveled / self.pixels_per_meter

            # Force player to keep up with scrolling (apply scroll effect)
            # This adds a constant force pushing right - ensure it's strong enough
            self.player.velocity_x = max(self.player.velocity_x, self.scroll_speed)

            # Move player with the adjusted velocity
            self.player.move(self.platforms)

            # Make sure player doesn't fall too far behind the scrolling
            if self.player.x < self.camera_offset_x - 200:
                self.game_manager.game_over = True
                self.game_manager.death_causes['left_behind'] += 1
                self.game_manager.end_timer()

            # Increase difficulty by slightly increasing scroll speed over time
            if pygame.time.get_ticks() % 1000 == 0:  # Every second
                self.scroll_speed += 0.01
                if self.scroll_speed > 7:  # Cap the maximum scroll speed
                    self.scroll_speed = 7

            # Generate new game elements
            self.generate_new_elements()

            if random.random() < 0.05:  # 5% chance per frame to check for new obstacles
                self.generate_obstacles()

            # Update moving obstacles
            self.update_moving_obstacles()

            # Update particles
            self.update_particles()

            # Update combo timer
            if self.combo_timer > 0:
                self.combo_timer -= 1
            else:
                self.combo_counter = 0  # Reset combo if timer expires

        # Check for coin collection
        for coin in self.coins:
            if not coin.collected and coin.check_collision(self.player.get_rect()):
                # Calculate coin value based on combo
                coin_value = coin.collect()

                # Apply combo multiplier if active
                if self.combo_timer > 0:
                    self.combo_counter += 1
                    # Increase value based on combo (max 3x multiplier)
                    combo_multiplier = min(3, 1 + self.combo_counter * 0.1)
                    coin_value = int(coin_value * combo_multiplier)
                else:
                    # Start a new combo
                    self.combo_counter = 1

                # Reset combo timer
                self.combo_timer = self.combo_timeout

                # Create particle effect
                self.create_coin_collect_particles(coin.x, coin.y)

                # Update player and score
                self.player.collect_coin(coin_value)
                self.game_manager.update_score(coin_value)

        # Check for obstacle collisions - GAME OVER
        for obstacle in self.obstacles:
            if self.player.get_rect().colliderect(obstacle.get_rect()):
                self.game_manager.game_over = True
                self.game_manager.death_causes['obstacle'] += 1
                self.game_manager.end_timer()
                break

        # Check if player fell off screen - GAME OVER
        if self.player.y > self.SCREEN_HEIGHT:
            self.game_manager.game_over = True
            self.game_manager.death_causes['falling'] += 1
            self.game_manager.end_timer()

        # Collect data point
        self.game_manager.collect_data_point(self.player)

        # Update player distance for statistics
        self.player.distance_traveled = self.distance_traveled

    def render(self):
        """Render the game"""
        # Fill background
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(self.BACKGROUND_COLOR)

        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen, self.camera_offset_x)

        # Draw coins
        for coin in self.coins:
            if not coin.collected:
                coin.draw(self.screen, self.camera_offset_x)

        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen, self.camera_offset_x)

        # Draw particles
        for particle in self.particles:
            pygame.draw.circle(
                self.screen,
                particle['color'],
                (int(particle['x'] - self.camera_offset_x), int(particle['y'])),
                int(particle['radius'])
            )

        # Draw player
        self.player.draw(self.screen, self.camera_offset_x)

        # Draw UI
        self.render_ui()

        # Update display
        pygame.display.flip()

    def render_ui(self):
        """Render UI elements"""
        # Draw score and coins
        score_text = self.font.render(f"Score: {self.player.score}", True, self.BLACK)
        coins_text = self.font.render(f"Coins: {self.player.coins_collected}", True, self.BLACK)
        distance_text = self.font.render(f"Distance: {int(self.distance_in_meters)} meters", True, self.BLACK)
        quit_text = self.font.render("Press Q to quit", True, self.BLACK)

        self.screen.blit(score_text, (20, 20))
        self.screen.blit(coins_text, (20, 50))
        self.screen.blit(distance_text, (20, 80))
        self.screen.blit(quit_text, (self.SCREEN_WIDTH - 150, 20))  # Add quit instructions in top-right

        # Draw combo counter if active
        if self.combo_timer > 0 and self.combo_counter > 1:
            combo_text = self.font.render(f"Combo: x{self.combo_counter}", True, (255, 140, 0))  # Orange color
            self.screen.blit(combo_text, (20, 110))

        # Draw game start instructions during delay
        if self.current_delay > 0:
            start_text = self.font.render("Use Arrow Keys to move and SPACE to jump", True, self.BLACK)
            self.screen.blit(start_text, (self.SCREEN_WIDTH // 2 - 200, self.SCREEN_HEIGHT // 2))

        # Draw game over message
        if self.game_manager.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Black with 50% transparency
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.font.render("Game Over!", True, self.WHITE)
            final_score = self.font.render(
                f"Final Score: {self.player.score} | Distance: {int(self.distance_in_meters)} meters", True, self.WHITE)

            # Get death cause
            death_cause = next((cause for cause, count in self.game_manager.death_causes.items()
                                if count > 0), "unknown")
            death_text = self.font.render(f"Cause of death: {death_cause}", True, self.WHITE)

            restart_text = self.font.render("Press R to restart or ESC to quit", True, self.WHITE)

            self.screen.blit(game_over_text, (self.SCREEN_WIDTH // 2 - 80, self.SCREEN_HEIGHT // 2 - 60))
            self.screen.blit(final_score, (self.SCREEN_WIDTH // 2 - 200, self.SCREEN_HEIGHT // 2 - 20))
            self.screen.blit(death_text, (self.SCREEN_WIDTH // 2 - 120, self.SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(restart_text, (self.SCREEN_WIDTH // 2 - 180, self.SCREEN_HEIGHT // 2 + 60))

        # Draw pause message
        if self.paused:
            # Semi-transparent overlay
            overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Black with 50% transparency
            self.screen.blit(overlay, (0, 0))

            pause_text = self.font.render("Paused - Press ESC to resume", True, self.WHITE)
            self.screen.blit(pause_text, (self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT // 2))

            # Add quit button instructions in pause menu
            quit_text = self.font.render("Press Q to quit to menu", True, self.WHITE)
            self.screen.blit(quit_text, (self.SCREEN_WIDTH // 2 - 120, self.SCREEN_HEIGHT // 2 + 40))

    def run(self):
        """Main game loop"""
        # Start timer
        self.game_manager.start_timer()

        while self.running:
            # Handle events
            self.handle_events()

            # Update game state
            self.update()

            # Render
            self.render()

            # Cap the frame rate
            self.clock.tick(self.FPS)

            # Check if game is over AND user presses ESC
            if self.game_manager.game_over and pygame.key.get_pressed()[pygame.K_ESCAPE]:
                # Save game stats before exiting
                self.game_manager.save_game_stats(self.player)
                self.running = False
                return
