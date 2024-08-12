from random import choice


class Apple:
    def __init__(self):
        self.coords = ()
        self.grid = {}
        self.is_alive = False

    def set_grid(self, grid):
        self.grid = grid

    def get_grid(self):
        return self.grid

    def spawn(self):
        spawn_possibilities = [coords for coords in self.grid.keys() if self.grid[coords] == 0]

        if len(spawn_possibilities) == 0:
            return

        self.grid[choice(spawn_possibilities)] = 2

        self.is_alive = True
