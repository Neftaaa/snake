import pygame


class Snake:
    def __init__(self, screen: pygame.Surface):
        self.apples_eaten = 0
        self.is_illegal_state = False
        self.screen = screen
        self.length = 3
        self.head_coords = (7, 7)
        self.is_outbound = False
        self.is_on_himself = False
        self.is_on_apple = False
        self.is_alive = True
        self.last_input = None
        self.grid = {}
        self.movements = ["None"]
        self.body = {0: (7, 7)}

    def set_grid(self, grid):
        self.grid = grid

    def get_grid(self):
        return self.grid

    def update_last_input(self):

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_UP] or keys[pygame.K_z]) and self.movements[-1] != "down" and self.movements[-1] != "up":
            self.last_input = "up"

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.movements[-1] != "left" and self.movements[-1] != "right":
            self.last_input = "right"

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.movements[-1] != "up" and self.movements[-1] != "down":
            self.last_input = "down"

        if (keys[pygame.K_LEFT] or keys[pygame.K_q]) and self.movements[-1] != "right" and self.movements[-1] != "left":
            self.last_input = "left"

    def head_movement(self):

        self.update_last_input()

        head_x = self.head_coords[0]
        head_y = self.head_coords[1]

        if self.last_input == "up":
            head_y -= 1
            self.movements.append("up")

        if self.last_input == "right":
            head_x += 1
            self.movements.append("right")

        if self.last_input == "down":
            head_y += 1
            self.movements.append("down")

        if self.last_input == "left":
            head_x -= 1
            self.movements.append("left")

        self.head_coords = (head_x, head_y)

        if self.head_coords not in self.grid.keys():
            self.is_outbound = True
            return

        if self.grid[self.head_coords] == 1 and self.length == len(self.body):
            self.is_on_himself = True
            return

        if self.grid[self.head_coords] == 2:
            self.is_on_apple = True
            self.length += 1
            self.apples_eaten += 1

        new_body = {}
        for key, value in self.body.items():
            if value not in new_body.values():
                new_body[key + 1] = value

        new_body[0] = self.head_coords
        self.body = new_body

        self.grid[self.head_coords] = 1

    def tail_movement(self):

        if len(self.body) > self.length:
            tail = max(self.body.keys())
            self.grid[self.body.pop(tail)] = 0

    def movement(self):
        self.head_movement()
        self.tail_movement()

    def check_state(self):
        if self.is_on_himself or self.is_outbound:
            self.is_illegal_state = True

    def kill(self):
        self.is_alive = False

    def update(self):

        if self.is_alive:
            self.movement()
            self.check_state()

            if self.is_illegal_state:
                self.kill()
