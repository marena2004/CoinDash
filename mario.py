import pygame
import sys
import random

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SKY_BLUE = (135, 206, 235)
BROWN = (139, 69, 19)
ORANGE = (210, 105, 30)
GOLD = (255, 223, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
FPS = 60

print("How to Play:")
print("- Use LEFT and RIGHT arrow keys to move.")
print("- Press SPACE to jump. You can double or triple jump!")
print("- Collect coins to increase your score.")
print("- Avoid falling off the screen or hitting obstacles.")

# Player Class
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
        self.image = pygame.image.load("mario.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.max_jumps = 30  # Allow double jump (change to 3 for triple)
        self.jumps_used = 0

    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.distance_traveled += abs(self.velocity[0])

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


# Coin Class
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


# Obstacle Class
class Obstacle:
    def __init__(self, position, size):
        self.position = list(position)
        self.size = size

    def check_collision(self, player):
        obstacle_rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        return player.rect().colliderect(obstacle_rect)

    def draw(self, screen):
        x, y = self.position
        width, height = self.size
        spike_color = (120, 0, 0)
        point1 = (x, y + height)
        point2 = (x + width // 2, y)
        point3 = (x + width, y + height)
        pygame.draw.polygon(screen, spike_color, [point1, point2, point3])


# Platform Class
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
            player.jumps_used = 0  # Reset jumps on landing

    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, pygame.Rect(self.position[0], self.position[1], self.width, self.height))
        pygame.draw.rect(screen, ORANGE, pygame.Rect(self.position[0], self.position[1], self.width, self.height), 3)


# Game Window
class GameWindow:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mario-Style Platformer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("comicsansms", 24)

    def render(self, player, platforms, coins, obstacles, game_over):
        self.screen.fill(SKY_BLUE)

        self.screen.blit(player.image, player.position)

        for platform in platforms:
            platform.draw(self.screen)

        for coin in coins:
            pygame.draw.circle(self.screen, GOLD, coin.position, coin.radius)

        for obstacle in obstacles:
            obstacle.draw(self.screen)

        score_text = self.font.render(f"Score: {player.score}", True, BLACK)
        jump_text = self.font.render(f"Jumps: {player.jump_count}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(jump_text, (10, 40))

        if game_over:
            over_text = self.font.render("Game Over! Press R to Restart.", True, RED)
            self.screen.blit(over_text, (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def update(self):
        self.clock.tick(FPS)


# Main Game Loop
def main():
    game_window = GameWindow()
    player = Player((100, 500))

    platforms = [
        Platform((i * 400, 550), 400, 50) for i in range(3)
    ] + [
        Platform((600, 480), 100, 20),
        Platform((750, 420), 100, 20),
        Platform((900, 360), 100, 20),
        Platform((1100, 300), 100, 20),
        Platform((1300, 240), 100, 20),
    ]

    coins = [Coin((i * 200 + 100, 500 - random.randint(0, 100))) for i in range(20)]
    obstacles = [Obstacle((i * 300 + 250, 530), (30, 30)) for i in range(10)]

    gravity = 1
    scroll_x = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if game_over and event.key == pygame.K_r:
                    main()

        keys = pygame.key.get_pressed()
        player.velocity[0] = 0
        if keys[pygame.K_LEFT]:
            player.velocity[0] = -5
        if keys[pygame.K_RIGHT]:
            player.velocity[0] = 5

        player.velocity[1] += gravity
        player.move()

        if player.position[1] > SCREEN_HEIGHT:
            game_over = True

        player.on_ground = False
        for platform in platforms:
            platform.check_collision(player)

        for obstacle in obstacles:
            if obstacle.check_collision(player):
                game_over = True

        coins = [coin for coin in coins if not coin.collect(player)]

        scroll_x = 0
        if player.position[0] > SCREEN_WIDTH // 2:
            scroll_x = player.position[0] - SCREEN_WIDTH // 2

        for platform in platforms:
            platform.position[0] -= scroll_x
            if platform.position[0] + platform.width < 0:
                platform.position[0] = SCREEN_WIDTH
                platform.position[1] = 550

        for coin in coins:
            coin.position[0] -= scroll_x
            if coin.position[0] + coin.radius < 0:
                coin.position[0] = SCREEN_WIDTH + random.randint(50, 200)
                coin.position[1] = 500 - random.randint(0, 100)

        for obstacle in obstacles:
            obstacle.position[0] -= scroll_x
            if obstacle.position[0] + obstacle.size[0] < 0:
                obstacle.position[0] = SCREEN_WIDTH + random.randint(50, 200)
                obstacle.position[1] = 530

        player.position[0] -= scroll_x

        game_window.render(player, platforms, coins, obstacles, game_over)
        game_window.update()


if __name__ == "__main__":
    main()
