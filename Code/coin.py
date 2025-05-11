import pygame


class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = (255, 215, 0)  # Gold color
        self.value = 10
        self.collected = False

    def draw(self, screen, camera_offset_x):
        """Draw the coin on screen with camera offset"""
        if self.collected:
            return

        # Apply camera offset for scrolling
        draw_x = self.x - camera_offset_x

        # Only draw if on screen
        if -self.radius * 2 <= draw_x <= screen.get_width():
            pygame.draw.circle(screen, self.color, (int(draw_x), int(self.y)), self.radius)

    def check_collision(self, player_rect):
        """Check if player has collected the coin"""
        coin_rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
        return coin_rect.colliderect(player_rect)

    def collect(self):
        """Mark coin as collected and return its value"""
        self.collected = True
        return self.value