import pygame
from src.Apple import Apple
from src.Snake import Snake


def restart_menu_inputs():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_r] or keys[pygame.K_SPACE]:
        return True

    if keys[pygame.K_ESCAPE]:
        return False

    return None


class Game:
    def __init__(self):
        self.fps_cap = 60
        self.game_speed = 10
        self.score = 0
        self.best_score = 0
        self.apple = None
        self.snake = None
        self.clock = None
        self.snake_default_coords = (7, 7)
        self.screen = None
        self.res = (800, 800)
        self.block_size = self.res[0] // 16
        self.grid_res = (16, 15)
        self.running = False
        self.grid = {}

    def window_initialisation(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption("Snake")
        self.screen.fill((50, 100, 50))
        self.clock = pygame.time.Clock()

    def grid_initialisation(self):
        for x in range(self.grid_res[0]):
            for y in range(self.grid_res[1]):
                self.grid[(x, y)] = 0

    def game_initialisation(self):
        self.grid_initialisation()
        self.snake = Snake(self.screen)
        self.snake.set_grid(self.grid)
        self.apple = Apple()
        self.apple.set_grid(self.grid)
        self.apple.spawn()

    def generate_new_grid(self):
        self.snake.update()
        self.grid = self.snake.get_grid()

        if self.snake.is_on_apple:
            self.apple.spawn()
            self.snake.is_on_apple = False
            self.grid = self.apple.get_grid()

    def draw_grid(self):

        colors = {0: (50, 100, 50), 1: (255, 55, 0), 2: (255, 0, 0)}

        for grid_x in range(self.grid_res[0]):
            for grid_y in range(self.grid_res[1]):
                screen_x = grid_x * 50
                screen_y = (grid_y + 1) * 50

                rect = pygame.Rect(screen_x, screen_y, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, colors[self.grid[(grid_x, grid_y)]], rect)

    def draw_panel(self):

        panel = pygame.Rect(0, 0, self.res[0], self.block_size)
        pygame.draw.rect(self.screen, (55, 70, 55), panel)

        frame = pygame.Rect(0, 0, self.res[0], self.res[1])
        pygame.draw.rect(self.screen, (0, 0, 0), frame, 3)

        outline = pygame.Rect(0, self.block_size, self.res[0], 3)
        pygame.draw.rect(self.screen, (0, 0, 0), outline, 2)

        self.score = self.snake.apples_eaten

        font = pygame.font.Font("freesansbold.ttf", 32)
        score_label = font.render(f"Score : {self.score}", True, "white")
        score_label_rect = score_label.get_rect()
        score_label_rect.topleft = (10, 12)
        self.screen.blit(score_label, score_label_rect)

        best_score_label = font.render(f"Best score : {self.best_score}", True, "white")
        best_score_label_rect = best_score_label.get_rect()
        best_score_label_rect.topright = (790, 12)
        self.screen.blit(best_score_label, best_score_label_rect)

    def draw_restart_menu(self):

        rect = pygame.Rect(0, 0, self.res[0] // 2, self.block_size * 3)
        rect.center = (self.res[0] // 2, self.res[1] // 2)
        pygame.draw.rect(self.screen, (55, 70, 55), rect)

        font = pygame.font.Font("freesansbold.ttf", 30)
        restart_label = font.render("Game over", True, "white")
        restart_label_rect = restart_label.get_rect()
        restart_label_rect.center = (self.res[0] // 2, (self.res[1] // 2) - 20)
        self.screen.blit(restart_label, restart_label_rect)

        keys_font = pygame.font.Font("freesansbold.ttf", 15)
        keys_label = keys_font.render("Press R or SPACE to restart or press ESCAPE to exit", True, "white")
        keys_label_rect = keys_label.get_rect()
        keys_label_rect.center = (self.res[0] // 2, (self.res[1] // 2) + 20)
        self.screen.blit(keys_label, keys_label_rect)

    def draw_win_menu(self):
        rect = pygame.Rect(0, 0, self.res[0] // 2, self.block_size * 3)
        rect.center = (self.res[0] // 2, self.res[1] // 2)
        pygame.draw.rect(self.screen, (55, 70, 55), rect)

        font = pygame.font.Font("freesansbold.ttf", 30)
        restart_label = font.render("You win ! GG", True, "white")
        restart_label_rect = restart_label.get_rect()
        restart_label_rect.center = (self.res[0] // 2, (self.res[1] // 2) - 20)
        self.screen.blit(restart_label, restart_label_rect)

        keys_font = pygame.font.Font("freesansbold.ttf", 15)
        keys_label = keys_font.render("Press R or SPACE to restart or press ESCAPE to exit", True, "white")
        keys_label_rect = keys_label.get_rect()
        keys_label_rect.center = (self.res[0] // 2, (self.res[1] // 2) + 20)
        self.screen.blit(keys_label, keys_label_rect)

    def run(self):
        frame_counter = 0
        self.running = True

        self.window_initialisation()

        self.game_initialisation()

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.clock.tick(self.fps_cap)

            if frame_counter % (self.fps_cap / self.game_speed) == 0:
                self.generate_new_grid()

            if self.score > self.best_score:
                self.best_score = self.score

            if self.snake.length == self.grid_res[0] * self.grid_res[1]:
                self.draw_win_menu()

            self.draw_grid()
            self.draw_panel()

            if not self.snake.is_alive:
                self.draw_restart_menu()

                is_restarting = restart_menu_inputs()

                if is_restarting:
                    self.game_initialisation()

                if is_restarting is False:
                    self.running = False

            pygame.display.flip()
            frame_counter += 1
            if frame_counter >= self.fps_cap:
                frame_counter = 0
