import pygame


class Obstacle:
    def __init__(self, position, width, height):
        self.position = list(position)
        self.width = width
        self.height = height

    def check_collision(self, player):
        return player.rect().colliderect(self.rect())

    def rect(self):
        return pygame.Rect(*self.position, self.width, self.height)
