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
RED = (200, 0, 0)
FPS = 60

# Instructions
print("How to Play:")
print("- Use LEFT and RIGHT arrow keys to move.")
print("- Press SPACE to jump.")
print("- Collect coins to increase your score.")
print("- Avoid falling off the screen or hitting obstacles.")

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

    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.width, self.height)


class Coin:
    def __init__(self, position, value=10):
        self.position = list(position)
        self.value = value
        self.radius = 10

    def collect(self, player):
        if pygame.Rect(player.rect()).collidepoint(self.position):
            player.collect_coin(self)
            return True
        return False


class Platform:
    def __init__(self, position, width, height):
        self.position = list(position)
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


class Obstacle:
    def __init__(self, position, width, height):
        self.position = list(position)
        self.width = width
        self.height = height

    def check_collision(self, player):
        obstacle_rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        return player.rect().colliderect(obstacle_rect)

    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.width, self.height)


class GameWindow:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)

    def render(self, player, platforms, coins, obstacles, game_over):
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, BLUE, player.rect())
        for platform in platforms:
            pygame.draw.rect(self.screen, BLACK, platform.rect())
        for coin in coins:
            pygame.draw.circle(self.screen, GOLD, coin.position, coin.radius)
        for obstacle in obstacles:
            pygame.draw.rect(self.screen, RED, obstacle.rect())

        # HUD
        score_text = self.font.render(f"Score: {player.score}", True, BLACK)
        jump_text = self.font.render(f"Jumps: {player.jump_count}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(jump_text, (10, 40))

        if game_over:
            over_text = self.font.render("Game Over! Press R to Restart.", True, RED)
            self.screen.blit(over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def update(self):
        self.clock.tick(FPS)


def main():
    game_window = GameWindow()
    player = Player((100, 500))
    platforms = [Platform((i * 400, 550), 400, 50) for i in range(10)]
    coins = [Coin((i * 200 + 100, 500)) for i in range(20)]
    obstacles = [Obstacle((i * 300 + 250, 530), 30, 20) for i in range(15)]
    gravity = 1
    scroll_x = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if game_over:
            if keys[pygame.K_r]:
                main()
            game_window.render(player, platforms, coins, obstacles, game_over)
            game_window.update()
            continue

        player.velocity[0] = 0
        if keys[pygame.K_LEFT]:
            player.velocity[0] = -5
        if keys[pygame.K_RIGHT]:
            player.velocity[0] = 5
        if keys[pygame.K_SPACE]:
            player.jump()

        player.velocity[1] += gravity
        player.move()

        # Stop game if player falls
        if player.position[1] > SCREEN_HEIGHT:
            game_over = True

        player.on_ground = False
        for platform in platforms:
            platform.check_collision(player)

        # Check for obstacle collision
        for obstacle in obstacles:
            if obstacle.check_collision(player):
                game_over = True

        # Check for coin collection
        coins = [coin for coin in coins if not coin.collect(player)]

        # Scroll the screen
        scroll_x = 0
        if player.position[0] > SCREEN_WIDTH // 2:
            scroll_x = player.position[0] - SCREEN_WIDTH // 2

        for platform in platforms:
            platform.position[0] -= scroll_x
        for coin in coins:
            coin.position[0] -= scroll_x
        for obstacle in obstacles:
            obstacle.position[0] -= scroll_x

        player.position[0] -= scroll_x

        game_window.render(player, platforms, coins, obstacles, game_over)
        game_window.update()


if __name__ == "__main__":
    main()
