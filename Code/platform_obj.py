import pygame


class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (0, 128, 0)  # Green color

    def get_rect(self):
        """Return pygame Rect for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, camera_offset_x):
        """Draw the platform on screen with camera offset"""
        # Apply camera offset for scrolling
        draw_x = self.x - camera_offset_x

        # Only draw if platform is (partially) on screen
        if draw_x + self.width >= 0 and draw_x <= screen.get_width():
            pygame.draw.rect(screen, self.color, (draw_x, self.y, self.width, self.height))