import random
from platform import Platform
from coin import Coin
from obstacle import Obstacle


class GameManager:
    def __init__(self):
        self.platforms = []
        self.coins = []
        self.obstacles = []
        self.last_platform_x = 600
        self.last_platform_y = 500

    def generate_initial_ground(self):
        for i in range(0, 1200, 300):
            self.platforms.append(Platform([i, 550], 300, 50))

    def generate_platforms(self):
        for _ in range(3):
            width = random.randint(100, 200)
            gap = random.randint(50, 150)
            new_x = self.last_platform_x + gap + width
            dy = random.randint(-80, 80)
            new_y = min(max(self.last_platform_y + dy, 200), 520)
            self.platforms.append(Platform([new_x, new_y], width, 20))
            ground_width = random.randint(300, 400)
            self.platforms.append(Platform([new_x, 550], ground_width, 50))
            if random.random() < 0.7:
                self.coins.append(Coin([new_x + width // 2, new_y - 30]))
            if random.random() < 0.3:
                self.obstacles.append(Obstacle([new_x + width // 2, new_y - 20], 30, 20))
            self.last_platform_x, self.last_platform_y = new_x, new_y

    def generate_ground(self):
        last_ground_x = max(p.position[0] + p.width for p in self.platforms if p.position[1] == 550)
        while last_ground_x < 1200:
            if random.random() < 0.1:
                last_ground_x += random.randint(80, 150)
            else:
                width = random.randint(200, 300)
                self.platforms.append(Platform([last_ground_x, 550], width, 50))
                last_ground_x += width

    def clean_up(self):
        self.platforms = [p for p in self.platforms if p.position[0] + p.width > -200]
        self.coins = [c for c in self.coins if c.position[0] > -100]
        self.obstacles = [o for o in self.obstacles if o.position[0] + o.width > -100]
