# platformer_game.py
import pygame
import sys
import random
from datetime import datetime

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GOLD = (255, 223, 0)
FPS = 60

# Instructions
print("How to Play:")
print("- Use LEFT and RIGHT arrow keys to move.")
print("- Press SPACE to jump.")
print("- Collect coins to increase your score.")
print("- Avoid falling off the screen.")
print("- Reach the end without dying!")

# Classes
class Player:
    def __init__(self, position):
        self.position = list(position)
        self.velocity = [0, 0]
        self.score = 0
        self.jump_count = 0
        self.coins_collected = 0
        self.distance_traveled = 0
        self.on_ground = False
        self.width, self.height = 50, 50

    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.distance_traveled += abs(self.velocity[0])

    def jump(self):
        if self.on_ground:
            self.velocity[1] = -15
            self.jump_count += 1
            self.on_ground = False

    def collect_coin(self, coin):
        self.score += coin.value
        self.coins_collected += 1

    def get_distance(self):
        return self.distance_traveled

    def get_jump_count(self):
        return self.jump_count

    def get_coins_collected(self):
        return self.coins_collected

    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.width, self.height)


class Coin:
    def __init__(self, position, value=10):
        self.position = position
        self.value = value
        self.radius = 10

    def collect(self, player):
        if pygame.Rect(player.rect()).collidepoint(self.position):
            player.collect_coin(self)
            return True
        return False


class Platform:
    def __init__(self, position, width, height):
        self.position = position
        self.width = width
        self.height = height

    def check_collision(self, player):
        player_rect = player.rect()
        platform_rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        if player_rect.colliderect(platform_rect) and player.velocity[1] >= 0:
            player.position[1] = self.position[1] - player.height
            player.velocity[1] = 0
            player.on_ground = True

    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.width, self.height)


class GameManager:
    def __init__(self):
        self.score = 0
        self.game_over = False
        self.death_count = 0
        self.completion_time = None
        self.start_time()

    def update_score(self, value):
        self.score += value

    def check_game_over(self, player):
        if player.position[1] > SCREEN_HEIGHT:
            self.game_over = True
            self.death_count += 1
            self.end_time()

    def start_time(self):
        self.start = datetime.now()

    def end_time(self):
        self.completion_time = datetime.now() - self.start


class GameWindow:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer Game")
        self.clock = pygame.time.Clock()

    def render(self, player, platforms, coins):
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, BLUE, player.rect())
        for platform in platforms:
            pygame.draw.rect(self.screen, BLACK, platform.rect())
        for coin in coins:
            pygame.draw.circle(self.screen, GOLD, coin.position, coin.radius)
        pygame.display.flip()

    def update(self):
        self.clock.tick(FPS)


def main():
    game_window = GameWindow()
    player = Player((100, 500))
    platforms = [Platform((0, 550), 800, 50), Platform((300, 400), 200, 20), Platform((600, 300), 150, 20)]
    coins = [Coin((320, 370)), Coin((650, 270))]
    game_manager = GameManager()

    gravity = 1

    while not game_manager.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.velocity[0] = 0
        if keys[pygame.K_LEFT]:
            player.velocity[0] = -5
        if keys[pygame.K_RIGHT]:
            player.velocity[0] = 5
        if keys[pygame.K_SPACE]:
            player.jump()

        player.velocity[1] += gravity
        player.move()

        for platform in platforms:
            platform.check_collision(player)

        coins = [coin for coin in coins if not coin.collect(player)]

        game_manager.check_game_over(player)
        game_window.render(player, platforms, coins)
        game_window.update()

    print(f"Game Over! Score: {player.score}, Jumps: {player.jump_count}, Coins: {player.coins_collected}")
    print(f"Completion Time: {game_manager.completion_time}")


if __name__ == "__main__":
    main()
