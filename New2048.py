import random
from numpy import array, zeros, rot90
import copy
import numpy as np


class Game2048:
    def __init__(self, n, tile_dist={2: 0.9, 4: 0.1}):
        self.n = n
        self.grid = [[0] * n for _ in range(n)]
        self.tile_dist = tile_dist  # probability distribution of tile values for spawning new tiles
        self.winner = None
        self.currentPlayer = 2  # 1 is user, 2 is adversery update after respective actions are played
        self.play_state = False  # True state means the game is ready to take player input.
        # False means adversary can decide the input to the game

        self.previous_state = self.grid
        self.previous_action = 0
        self.game_count = 0
        self.game_history = {}

    def _get_empty_cells_(self):
        """
         abstract method to get list of empty cells
         :return: array of empty cell positions available
         """
        empty_cells = []
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))

        return empty_cells

    def start_game(self):
        """
        starts the game with a randomly positioned tile
        :return: None, turns play_state flag to True
        """
        # empty_cells = self._get_empty_cells_()
        # if self._get_empty_cells_():
        #     i, j = random.choice(empty_cells)
        #     self.grid[i][j] = 2 if random.random() < 0.9 else 4
        self.playAdversaryAction()
        self.play_state = True

    def try_action(self, action):
        grid = self.grid
        rotated_board = rot90(grid, action)
        cols = [rotated_board[i, :] for i in range(self.n)]
        grid = [self._move_col_left_(col) for col in cols]
        grid = rot90(grid, -action)
        return grid
    
    def _move_col_left_(self, arr):
        temp = []
        ind = 0
        n = []
        #print(arr.size)
        i = 0
        while i < len(arr):
            foun = False
            f = 0
            s = 0
            for j in range(i, len(arr)):
                if arr[j] != 0 and not foun:
                    f = arr[j]
                    foun = True

                elif(arr[j] != 0):
                    s = arr[j]
                    i = j
                    break
            if len(temp) != 0:
                temp.append((temp[-1][-1], f))
            temp.append((f, s))
            i +=1
        temp.append((s,0))
        #print(temp)

        to_ret = np.zeros(len(arr))
        ind = 0
        cp = temp.copy()
        flag = False
        for i in range(len(temp)):
            try:
                if temp[i][0] == temp[i][1]:
                    to_ret[ind] = temp[i][0]*2
                    if i != len(temp)-1:
                        flag = True
                        #print("wowowo")
                        temp.pop(i+1)

                else:

                    to_ret[ind] = temp[i][0]
                ind +=1
            except:
                pass
        return to_ret
    
    '''
    def _move_col_left_(self, col):
        new_column = zeros(self.n, dtype=col.dtype)
        j = 0
        previous = None
        for i in range(col.size):
            if col[i] != 0:  # number different from zero
                if previous is None:
                    previous = col[i]
                else:
                    if previous == col[i]:
                        new_column[j] = 2 * col[i]
                        j += 1
                        previous = None
                    else:
                        new_column[j] = previous
                        j += 1
                        previous = col[i]
        if previous is not None:
            new_column[j] = previous
        return new_column'''

    def _are_grids_equal_(self,list1, list2):
        # Check if the dimensions are the same
        if len(list1) != len(list2) or any(len(row1) != len(row2) for row1, row2 in zip(list1, list2)):
            return False

        # Check each element
        for row1, row2 in zip(list1, list2):
            for elem1, elem2 in zip(row1, row2):
                if elem1 != elem2:
                    return False

        # Lists are equal
        return True

    def get_user_actions(self):
        # returns possible user actions as np array based on state
        #   possible actions 1(up) and/or 2(right) and/or 3(down) and/or 4(left)
        # if self.play_state:  # game is play state
        #     print("Game is in player mode: user action required")
        #     return None
        # else:
        #     if self.previous_action:  # if the previous action is not the first action
                actions = []
                for i in [1, 2, 3, 4]:
                    # print(( self.grid ,self.try_action(i)))
                    if not self._are_grids_equal_( self.grid ,self.try_action(i)):
                        actions.append(i)

                return array(actions)


        # pass

    def playRandUser(self):
        # given possible actions plays one randomly
        #   (calling playUserAction might be useful)
        if not self.play_state:
            print('<Func playRandUser>Game not in player mode: adversary action required')
            return None
        else:
            actions = self.get_user_actions()
            # print(actions)
            action = np.random.choice(actions)
            self.playUserAction(action)
            self.previous_action = action
        pass

    def playUserAction(self, action):
        """
        :param action:
        :return: None, changes game state to False
        """
        # given an action play that action
        if self.play_state:
            self.grid = self.try_action(action)
            self.previous_action = action
            self.play_state = False
            self.check_winner()
        else:
            print(f'<func playUserAction>Game not in player mode: adversary action required, game state: {self.play_state}')
            return None


        pass

    def getAdverseryActions(self):
        """
        Works only if game state is in adversary mode
        :return: a list of lists with each list having first element as the tile-number
        and the second element as the coordinate of that tile.
        """
        # returns possible user actions as np array based on state
        #   possible actions empty spaces on board as well as the number it can spawn
        if self.play_state:
            print('<Func aetAdversaryActions>Game is in player mode: user action required')
        else:
            adv_actions = [i for i in self._get_empty_cells_()]
            return adv_actions
        pass

    def playRandAdverseryAction(self):
        # given possible actions play one at random
        #   (calling playAdverseryAction might be useful)
        self._generate_new_tile_()



        pass

    def _generate_new_tile_(self):
        """
        Generates a new ti,e with values and position
        :return: list [tile_value, (tile_position_x,tile_position_y)]
        """
        keys, probabilities = zip(*self.tile_dist.items())
        selected_tile_value = random.choices(keys, probabilities)[0]
        selected_tile_position = random.choice(self._get_empty_cells_())
        return [selected_tile_value, selected_tile_position]

    def playAdversaryAction(self):
        # spawns a new tile
        if self.play_state:
            print('<Func playAdversaryAction>Game is in player mode: user action required')
        else:
            tile = self._generate_new_tile_()
            # print(tile)

            tile_value, tile_position = tile[0], tile[1]
            # print(type(tile_position[0]), tile_position[1])
            self.grid[tile_position[0]][tile_position[1]] = tile_value
            self.play_state = True

            self.game_count += 1
            self.game_history[self.game_count] = {'action': self.previous_action, 'adversary': tile}
            self.check_game_over()

        pass

    def copy(self):
        # deep copy the game/class
        return copy.deepcopy(self)
        pass

    def check_winner(self):
        # check if 2048 is reached(uaer win) or if game board is full with no possible user actions(ad win)
        if 2048 in self.grid:
            self.winner = 1
            return True
        else:
            return False

    def check_game_over(self):
        if len(self.get_user_actions()) == 0:  # no actions possible: Game over
            self.winner = 2
            return True
        else:
            return False

        pass

    def get_highest_tile(self):
        return max(element for sublist in self.grid for element in sublist)
    
    def play_random_moves_until_done(self):
        while self.winner == None:
            if self.check_winner:
                return 1
            if self.check_game_over:
                return -1
            if self.play_state:
                self.playRandUser()
            else:
                self.playAdversaryAction()
            

    def __str__(self):
        # to string displaying board
        result = ""
        for row in self.grid:
            result += "+------" * len(row) + "+\n"
            result += "|"
            for cell in row:
                if cell == 0:
                    result += "{:^6}|".format(" ")
                else:
                    result += "{:^6}|".format(int(cell))
            result += "\n"

        result += "+------" * len(row) + "+"
        return result

#todo More work on saving history of a game and playing a game from a history


def main():
    ################################################################################
    #                             GAME PLAY                                        #
    ################################################################################
    # game = Game2048(4)
    # game.start_game()
    # print(str(game))
    # game.playUserAction(1)
    # print(str(game))
    # game.play_= True
    # game.playUserAction(2)
    # print(str(game))
    # game.play_state = True
    # game.playUserAction(3)
    # print(str(game))
    # game.play_state = True
    # game.playUserAction(4)
    # print(str(game))
    # print(game.play_state)
    # game.playAdversaryAction()
    # print(game)
    # game.playRandUser()
    # print(game)

    game = Game2048(6)
    game.start_game()
    # for i in range(10):
    #     game.playRandUser()
    #     print(game)
    #     game.playAdversaryAction()
    #     print(game)

    while not game.check_game_over():
    # while not game.check_game_over() and not game.check_winner():
        game.playRandUser()
        # print(game)
        game.playAdversaryAction()
        print(game)

    print(game.get_highest_tile())