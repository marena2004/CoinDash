import pygame
import sys
import random

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GOLD = (255, 223, 0)
RED = (200, 0, 0)
FPS = 60
SCROLL_SPEED = 4


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


class Platform:
    def __init__(self, position, width, height):
        self.position = list(position)
        self.width = width
        self.height = height

    def check_collision(self, player):
        rect = player.rect()
        plat_rect = pygame.Rect(*self.position, self.width, self.height)
        if rect.colliderect(plat_rect) and player.velocity[1] >= 0:
            player.position[1] = self.position[1] - player.height
            player.velocity[1] = 0
            player.on_ground = True

    def rect(self):
        return pygame.Rect(*self.position, self.width, self.height)


class Coin:
    def __init__(self, position, value=10):
        self.position = list(position)
        self.value = value
        self.radius = 10

    def collect(self, player):
        if player.rect().collidepoint(self.position):
            player.collect_coin(self)
            return True
        return False


class Obstacle:
    def __init__(self, position, width, height):
        self.position = list(position)
        self.width = width
        self.height = height

    def check_collision(self, player):
        return player.rect().colliderect(self.rect())

    def rect(self):
        return pygame.Rect(*self.position, self.width, self.height)


class GameWindow:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Side-Scrolling Platformer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)

    def render(self, player, platforms, coins, obstacles, game_over):
        self.screen.fill(WHITE)

        # Draw player (fixed X position)
        pygame.draw.rect(self.screen, BLUE, player.rect())

        for platform in platforms:
            pygame.draw.rect(self.screen, BLACK, platform.rect())
        for coin in coins:
            pygame.draw.circle(self.screen, GOLD, (int(coin.position[0]), int(coin.position[1])), coin.radius)
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

    def show_start_screen(self):
        self.screen.fill(WHITE)
        start_text = self.font.render("Press SPACE to Start", True, BLACK)
        self.screen.blit(start_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        pygame.display.flip()


def main():
    game_window = GameWindow()
    player = Player([100, 500])
    platforms = []
    coins = []
    obstacles = []
    gravity = 1
    game_over = False

    game_window.show_start_screen()

    # Wait for spacebar press to start game
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_input = False  # Start the game when space is pressed

    # Generate initial ground
    for i in range(0, SCREEN_WIDTH + 400, 300):
        platforms.append(Platform([i, 550], 300, 50))

    # Procedural generation
    def generate_platforms(last_x, last_y):
        for _ in range(3):
            width = random.randint(100, 200)
            gap = random.randint(50, 150)
            new_x = last_x + gap + width
            dy = random.randint(-80, 80)
            new_y = min(max(last_y + dy, 200), 520)
            platforms.append(Platform([new_x, new_y], width, 20))

            # Add a ground segment
            ground_width = random.randint(300, 400)
            platforms.append(Platform([new_x, 550], ground_width, 50))

            if random.random() < 0.7:
                coins.append(Coin([new_x + width // 2, new_y - 30]))

            if random.random() < 0.3:
                obstacles.append(Obstacle([new_x + width // 2, new_y - 20], 30, 20))

            last_x, last_y = new_x, new_y
        return last_x, last_y

    def generate_ground(last_x):
        while last_x < SCREEN_WIDTH + 400:
            # 10% chance to create a small gap
            if random.random() < 0.1:
                gap_size = random.randint(80, 150)
                last_x += gap_size  # skip that part of the ground
            else:
                ground_width = random.randint(200, 300)
                platforms.append(Platform([last_x, 550], ground_width, 50))
                last_x += ground_width
        return last_x




    def generate_coins(platform):
        # Place coins at random positions along the platform
        num_coins = random.randint(3, 6)  # Generate more coins (3 to 6 coins per platform)
        for _ in range(num_coins):
            x_position = platform.position[0] + random.randint(0, platform.width)
            y_position = platform.position[1] - random.randint(30, 70)  # Coins will float above the platform
            coins.append(Coin([x_position, y_position]))

    # for platform in platforms:
    #     generate_coins(platform)

    last_platform_x, last_platform_y = 600, 500
    last_platform_x, last_platform_y = generate_platforms(last_platform_x, last_platform_y)

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

        if keys[pygame.K_SPACE]:
            player.jump()

        # Physics
        player.velocity[1] += gravity
        player.move()

        # Game over if fall off screen
        if player.position[1] > SCREEN_HEIGHT:
            game_over = True

        # Platform collision
        player.on_ground = False
        for platform in platforms:
            platform.check_collision(player)

        # Coin collection
        coins = [c for c in coins if not c.collect(player)]

        # Obstacle collision
        for obs in obstacles:
            if obs.check_collision(player):
                game_over = True

        # Scroll world
        for platform in platforms:
            platform.position[0] -= SCROLL_SPEED
        for coin in coins:
            coin.position[0] -= SCROLL_SPEED
        for obs in obstacles:
            obs.position[0] -= SCROLL_SPEED

        # Continue the main ground with occasional gaps
        last_ground_x = max(p.position[0] + p.width for p in platforms if p.position[1] == 550)
        last_ground_x = generate_ground(last_ground_x)

        # Generate new platforms
        if platforms[-1].position[0] < SCREEN_WIDTH + 300000:
            last_platform_x, last_platform_y = generate_platforms(last_platform_x, last_platform_y)

        # Continuously generate ground with smaller gaps
        ground_platforms = [p for p in platforms if p.position[1] == 550]
        if ground_platforms:
            last_ground_x = max(p.position[0] + p.width for p in ground_platforms)
            if last_ground_x < SCREEN_WIDTH + 100:  # Trigger earlier
                ground_width = random.randint(200, 250)  # Smaller chunks
                platforms.append(Platform([last_ground_x, 550], ground_width, 50))


        # Remove off-screen objects
        platforms = [p for p in platforms if p.position[0] + p.width > -200]
        coins = [c for c in coins if c.position[0] > -100]
        obstacles = [o for o in obstacles if o.position[0] + o.width > -100]



        game_window.render(player, platforms, coins, obstacles, game_over)
        game_window.update()


if __name__ == "__main__":
    main()
