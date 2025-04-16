import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GOLD = (255, 223, 0)
RED = (200, 0, 0)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60


class GameWindow:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("CoinDash")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)

    def render(self, player, platforms, coins, obstacles, game_over):
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, BLUE, player.rect())

        for platform in platforms:
            pygame.draw.rect(self.screen, BLACK, platform.rect())
        for coin in coins:
            pygame.draw.circle(self.screen, GOLD, (int(coin.position[0]), int(coin.position[1])), coin.radius)
        for obstacle in obstacles:
            pygame.draw.rect(self.screen, RED, obstacle.rect())

        self.screen.blit(self.font.render(f"Score: {player.score}", True, BLACK), (10, 10))
        self.screen.blit(self.font.render(f"Jumps: {player.jump_count}", True, BLACK), (10, 40))

        if game_over:
            self.screen.blit(self.font.render("Game Over! Press R to Restart.", True, RED),
                             (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def update(self):
        self.clock.tick(FPS)

    def show_start_screen(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.font.render("Press SPACE to Start", True, BLACK),
                         (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        pygame.display.flip()
