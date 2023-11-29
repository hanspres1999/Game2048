import random
from numpy import array, zeros, rot90


class Game2048:
    def __init__(self, n, adversary, ):
        self.n = n
        self.grid = [[0] * n for _ in range(n)]
        self.end = False
        # self.play_game()
        # self.new_tile()
        # self.new_tile()

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

    def move_col_left(self, col):
        new_col = zeros(self.n, dtype=col.dtype)
        j = 0
        previous = None
        for i in range(col.size):
            if col[i] != 0:  # number different from zero
                if previous is None:
                    previous = col[i]
                else:
                    if previous == col[i]:
                        new_col[j] = 2 * col[i]
                        j += 1
                        previous = None
                    else:
                        new_col[j] = previous
                        j += 1
                        previous = col[i]
        if previous is not None:
            new_col[j] = previous
        return new_col

    def move(self, direction):
        # 0: left, 1: up, 2: right, 3: down
        rotated_board = rot90(self.grid, direction)
        cols = [rotated_board[i, :] for i in range(self.n)]
        self.grid = [self.move_col_left(col) for col in cols]
        self.grid = rot90(self.grid, -direction)

        self.new_tile()

    def move_left(self):
        self.move(1)

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

    def get_action(self):
        self.print_grid()
        action = input("a: Left, d:right, w:up, s:down")
        dirs = {'a': 0, 'w': 1, 'd': 2, 's': 3}
        while not self.game_over():
            action = input("a: Left, d:right, w:up, s:down")

        return action

    def play_game(self,action):
        self.move(dirs[dir])

    def get_action(self):
        '''gets a move '''
        dirs = {'a': 0, 'w': 1, 'd': 2, 's': 3}
        while not self.game_over():
            dir = self.get_input()
            self.move(dirs[dir])



#todo: Add error handelling on user inputs
#todo: Keep a count of max tile and current score
#todo: find a way to keep a record of states, actions and transitions.