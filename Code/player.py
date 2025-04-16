import pygame

class Player:
    def __init__(self, position):
        self.position = list(position)
        self.velocity = [0, 0]
        self.width, self.height = 50, 50
        self.jump_count = 0
        self.score = 0
        self.coins_collected = 0
        self.on_ground = False
        self.max_jumps = 2000
        self.jumps_used = 0

    def move(self):
        self.position[1] += self.velocity[1]

    def jump(self):
        if self.jumps_used < self.max_jumps:
            self.velocity[1] = -15
            self.jump_count += 1
            self.jumps_used += 1
            self.on_ground = False

    def collect_coin(self, coin):
        self.score += coin.value
        self.coins_collected += 1

    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.width, self.height)
