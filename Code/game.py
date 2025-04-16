import pygame
import sys
from player import Player
from game_window import GameWindow
from game_manager import GameManager

GRAVITY = 1
SCROLL_SPEED = 4
SCREEN_HEIGHT = 600


class Game:
    def __init__(self):
        pygame.init()
        self.window = GameWindow()
        self.manager = GameManager()
        self.player = Player([100, 500])
        self.game_over = False

    def start_screen(self):
        self.window.show_start_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        self.start_screen()
        self.manager.generate_initial_ground()
        self.manager.generate_platforms()

        while True:
            self.handle_events()
            keys = pygame.key.get_pressed()

            if self.game_over:
                if keys[pygame.K_r]:
                    self.__init__()  # Restart game cleanly
                    self.run()
                    return
                self.window.render(self.player, self.manager.platforms, self.manager.coins, self.manager.obstacles,
                                   self.game_over)
                self.window.update()
                continue

            if keys[pygame.K_SPACE]:
                self.player.jump()

            self.player.velocity[1] += GRAVITY
            self.player.move()

            if self.player.position[1] > SCREEN_HEIGHT:
                self.game_over = True

            self.player.on_ground = False
            for platform in self.manager.platforms:
                platform.check_collision(self.player)

            self.manager.coins = [coin for coin in self.manager.coins if not coin.collect(self.player)]

            for obstacle in self.manager.obstacles:
                if obstacle.check_collision(self.player):
                    self.game_over = True

            for obj_list in [self.manager.platforms, self.manager.coins, self.manager.obstacles]:
                for obj in obj_list:
                    obj.position[0] -= SCROLL_SPEED

            self.manager.generate_ground()
            if self.manager.platforms[-1].position[0] < 30000:
                self.manager.generate_platforms()
            self.manager.clean_up()

            self.window.render(self.player, self.manager.platforms, self.manager.coins, self.manager.obstacles,
                               self.game_over)
            self.window.update()
