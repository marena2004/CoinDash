import pygame

class Platform:
    def __init__(self, position, width, height):
        self.position = list(position)
        self.width = width
        self.height = height

    def check_collision(self, player):
        if player.rect().colliderect(self.rect()) and player.velocity[1] >= 0:
            player.position[1] = self.position[1] - player.height
            player.velocity[1] = 0
            player.on_ground = True

    def rect(self):
        return pygame.Rect(*self.position, self.width, self.height)
