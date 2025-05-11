import pygame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 50

        # Try to load player sprite, use fallback if not found
        try:
            self.sprite = pygame.image.load("player.png").convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
            self.use_sprite = True
        except:
            self.use_sprite = False
            self.color = (0, 0, 255)  # Blue color

        # Movement properties
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration_x = 0.5
        self.friction = 0.1
        self.gravity = 0.5
        self.jump_strength = -12
        self.max_velocity_x = 8
        self.max_velocity_y = 15
        self.on_ground = False  # Will be properly set in the first move() call

        # Game statistics
        self.score = 0
        self.coins_collected = 0
        self.jump_count = 0
        self.distance_traveled = 0

        # Animation state
        self.facing_right = True
        self.is_jumping = False

    def move(self, platforms):
        """Handle player movement and physics"""
        # Get keyboard input
        keys = pygame.key.get_pressed()

        # Horizontal movement - increase acceleration for more responsive controls
        if keys[pygame.K_LEFT]:
            self.velocity_x -= self.acceleration_x * 1.2  # Slightly more responsive
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.velocity_x += self.acceleration_x * 1.2  # Slightly more responsive
            self.facing_right = True

        # Apply friction only if not pressing movement keys
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and abs(self.velocity_x) > 0:
            friction_force = min(abs(self.velocity_x), self.friction)
            if self.velocity_x > 0:
                self.velocity_x -= friction_force
            else:
                self.velocity_x += friction_force

        # Limit maximum velocity
        self.velocity_x = max(-self.max_velocity_x, min(self.velocity_x, self.max_velocity_x))
        self.velocity_y = max(-self.max_velocity_y, min(self.velocity_y, self.max_velocity_y))

        # Apply gravity only if not on ground
        if not self.on_ground:
            self.velocity_y += self.gravity

        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Reset ground status before checking collisions
        old_on_ground = self.on_ground
        self.on_ground = False
        self.is_jumping = self.velocity_y < 0

        # Check for platform collisions
        for platform in platforms:
            # First check if player is directly on top of a platform
            if self.check_standing_on_platform(platform):
                self.on_ground = True
                self.velocity_y = 0
                # Place player on top of platform
                self.y = platform.y - self.height
                break
            # Then check for collision while falling
            elif self.check_platform_collision(platform):
                self.on_ground = True
                self.velocity_y = 0
                # Place player on top of platform
                self.y = platform.y - self.height
                break

    def check_standing_on_platform(self, platform):
        """Check if player is standing directly on a platform without falling"""
        # Check if player is within platform x bounds
        if self.x + self.width < platform.x or self.x > platform.x + platform.width:
            return False

        # Check if player's feet are exactly at the platform top
        player_feet = self.y + self.height
        platform_top = platform.y

        # Allow a small margin of error (2 pixels instead of 1)
        return abs(player_feet - platform_top) <= 2

    def check_platform_collision(self, platform):
        """Check if player is colliding with a platform while falling"""
        # Only check if player is falling
        if self.velocity_y < 0:
            return False

        # Check if player is within platform x bounds
        if self.x + self.width < platform.x or self.x > platform.x + platform.width:
            return False

        # Check if player is landing on platform (feet touch platform)
        player_feet = self.y + self.height
        platform_top = platform.y

        # Check if player's feet are at or below the platform top,
        # and were above the platform top in the previous frame
        if player_feet >= platform_top and player_feet - self.velocity_y < platform_top:
            return True

        return False

    def jump(self):
        """Make the player jump if on ground"""
        if self.on_ground:
            self.velocity_y = self.jump_strength
            # self.on_ground = False
            self.is_jumping = True
            self.jump_count += 1

    def get_rect(self):
        """Return pygame Rect for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, camera_offset_x):
        """Draw the player on screen with camera offset"""
        # Apply camera offset for scrolling
        draw_x = self.x - camera_offset_x

        # Only draw if player is on screen
        if -self.width <= draw_x <= screen.get_width():
            # Draw player using sprite or rectangle
            if self.use_sprite:
                # Flip sprite based on direction
                sprite = pygame.transform.flip(self.sprite, not self.facing_right, False)
                screen.blit(sprite, (draw_x, self.y))
            else:
                # Draw with different colors based on state
                color = self.color
                if self.is_jumping:
                    color = (100, 100, 255)  # Lighter blue when jumping
                elif not self.on_ground:
                    color = (50, 50, 200)  # Darker blue when falling

                pygame.draw.rect(screen, color, (draw_x, self.y, self.width, self.height))

                # Draw eyes to show direction
                eye_size = 5
                eye_y = self.y + 10

                if self.facing_right:
                    # Right-facing eyes
                    eye1_x = draw_x + self.width - 10
                    eye2_x = draw_x + self.width - 20
                else:
                    # Left-facing eyes
                    eye1_x = draw_x + 5
                    eye2_x = draw_x + 15

                pygame.draw.circle(screen, (255, 255, 255), (eye1_x, eye_y), eye_size)
                pygame.draw.circle(screen, (255, 255, 255), (eye2_x, eye_y), eye_size)

    def collect_coin(self, value):
        """Update player stats when collecting a coin"""
        self.coins_collected += 1
        self.score += value

    def get_distance(self):
        """Get the distance traveled by player"""
        return self.distance_traveled

    def get_coins_collected(self):
        """Get the number of coins collected"""
        return self.coins_collected

    def get_jump_count(self):
        """Get the number of jumps performed"""
        return self.jump_count