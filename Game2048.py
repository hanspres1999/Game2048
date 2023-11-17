import random

class Game:
    def __init__(self, n):
        self.n = n
        self.grid = [[0] * n for _ in range(n)]
        self.new_tile()
        self.new_tile()

    def new_tile(self):
        empty_cells = []
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))

        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def print_grid(self):
        for row in self.grid:
            print("| " + " | ".join(str(tile) for tile in row) + " |")

    def move_left(self):
        for row in self.grid:
            new_row = []
            for tile in row:
                if tile != 0:
                    new_row.append(tile)

            while len(new_row) < self.n:
                new_row.append(0)

            self.grid[row.index(new_row[0])] = new_row

    def move_right(self):
        for row in self.grid:
            new_row = []
            for tile in reversed(row):
                if tile != 0:
                    new_row.append(tile)

            while len(new_row) < self.n:
                new_row.append(0)

            self.grid[row.index(new_row[0])] = new_row[::-1]

    def move_up(self):
        for col in range(self.n):
            new_col = []
            for row in range(self.n):
                tile = self.grid[row][col]
                if tile != 0:
                    new_col.append(tile)

            while len(new_col) < self.n:
                new_col.append(0)

            for row in range(self.n):
                self.grid[row][col] = new_col[row]

    def move_down(self):
        for col in range(self.n):
            new_col = []
            for row in reversed(range(self.n)):
                tile = self.grid[row][col]
                if tile != 0:
                    new_col.append(tile)

            while len(new_col) < self.n:
                new_col.append(0)

            for row in reversed(range(self.n)):
                self.grid[row][col] = new_col[row]

    def game_over(self):
        for row in self.grid:
            for tile in row:
                if tile == 0:
                    return False

        for i in range(self.n):
            for j in range(self.n - 1):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return False

        for i in range(self.n - 1):
            for j in range(self.n):
                if self.grid[i][j] == self.grid[i + 1][j]:
                    return False

        return True

