import numpy as np
import matplotlib.pyplot as plt
import copy
from Board import Board
class ConnectBoard(Board):

    # rows
    #     #@params
    #     #= # of rows (default 6)
    # cols = # of cols (default 7)
    # win_span = # in a row for a win (default 4 because it's connect4 lol)
    #

    def __init__(self, players=[], rows=6, cols=7, win_span=4):
        super().__init__(players, rows, cols)
       # self.init_board[self.init_board == 0] = -1
        self.win_span = win_span

        self.high = []
        for c in range(cols):
            self.high.append(0)

    def get_state(self, player):
        string = ""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.get(r,c) == player:
                    string += "1"
                elif self.get(r,c) in self.players:
                    string += "2"
                else:
                    string += "0"
        return string

    def __deepcopy__(self, memodict={}):

        newBoard = Board(self.players, self.rows, self.cols, self.win_span)
        newBoard.board = np.copy(self.board)
        newBoard.turn = self.turn
        newBoard.game_over = self.game_over
        newBoard.moves = copy.copy(self.moves)
        return newBoard



    def place(self, col):
        if 0 <= col < self.cols:
            if int(self.check_win(True)) > 0:
                return False

            for r in range(self.rows - 1, -1, -1):
                if self.board[r,col] == 0:
                    self.board[r,col] = int(self.get_player_turn());
                    self.turn += 1
                    self.moves.append(col)
                    return True
        return False

    def __deepcopy__(self, memodict={}):
        newBoard = ConnectBoard(self.players, self.rows, self.cols, self.win_span)
        newBoard.board = np.copy(self.board)
        newBoard.turn = self.turn
        newBoard.game_over = self.game_over
        newBoard.moves = copy.deepcopy(self.moves)
        newBoard.winner = self.winner
        return newBoard

    def get_players(self):
        return self.players


    def get_actions(self):
        available = []
        for c in range(self.cols):
            if self.board[0, c] == 0:
                available.append(c)

        if len(available) == 0:
            self.game_over = True

        return available


    ##Get a one hot vector of the last move
    def get_last_action(self):
        move = self.get_last_move()
        vector = []

        for i in range(self.cols):
            if i == move:
                vector.append(1)
            else:
                vector.append(0)
        return vector

    def get_last_move(self):
        if len(self.moves) == 0:
            return -1
        return self.moves[len(self.moves) - 1]

    def get_neighbours(self, r, c):
        map = {"LEFT":[], "RIGHT":[], "UP":[], "DOWN":[], "UP_LEFT":[], "DOWN_RIGHT":[], "UP_RIGHT":[], "DOWN_LEFT":[]}
        if c >= 0 and c < self.cols and r >= 0 and r < self.rows:

            cell_to_check = self.get_c(r, c)

            if cell_to_check > 0:
                ##get left

                for col in range(c - 1, c - self.win_span , -1):
                    neighbour_cell = self.get_c(r, col)
                    map["LEFT"].append(neighbour_cell)
                ##get right

                for col in range(c + 1, c + self.win_span, 1):
                    neighbour_cell = self.get_c(r, col)

                    if neighbour_cell >= 0:
                        map["RIGHT"].append(neighbour_cell)

                ##get up
                for row in range(r - 1, r - self.win_span, -1):
                    neighbour_cell = self.get_c(row, c)
                    if neighbour_cell >= 0:
                        map["UP"].append(neighbour_cell)

                ##get down
                for row in range(r + 1, r + self.win_span, 1):
                    neighbour_cell = self.get_c(row, c)
                    if neighbour_cell >= 0:
                        map["DOWN"].append(neighbour_cell)

                ##get up_left

                for i in range(self.win_span - 1):
                    row = r - (i + 1)
                    col = c - (i + 1)
                    neighbour_cell = self.get_c(row, col)
                    if neighbour_cell >= 0:
                        map["UP_LEFT"].append(neighbour_cell)

                ##get down_right
                for i in range(self.win_span - 1):
                    row = r + (i + 1)
                    col = c + (i + 1)
                    neighbour_cell = self.get_c(row, col)
                    if neighbour_cell >= 0:
                        map["DOWN_RIGHT"].append(neighbour_cell)

                ##get bottom_left

                temp_row = r + 1
                temp_col = c - 1
                for i in range(self.win_span):
                    neighbour_cell = self.get_c(temp_row, temp_col)

                    if neighbour_cell >= 0:
                        map["DOWN_LEFT"].append(neighbour_cell)
                    temp_row += 1
                    temp_col -= 1

                ##get up right
                temp_row = r - 1
                temp_col = c + 1

                for i in range(self.win_span - 1):
                    neighbour_cell = self.get_c(temp_row, temp_col)

                    if neighbour_cell >= 0:
                        map["UP_RIGHT"].append(neighbour_cell)
                    temp_row -= 1
                    temp_col += 1
        return map


    def check_win(self, step = False):

        cells_to_check = []

        if step:
            C = self.get_last_move()
            R = self.cols
            cells_to_check.append((self.get(R,C), R, C))
        else:
            for r in range(self.rows):
                for c in range(self.cols):
                    cells_to_check.append((self.get(r,c), r, c))

        for r in range(self.rows):
            for c in range(self.cols):
                cells_to_check.append((self.get_c(r,c), r, c))

        for cell_to_check_tuple in cells_to_check:
            cell_to_check = cell_to_check_tuple[0]
            r = cell_to_check_tuple[1]
            c = cell_to_check_tuple[2]

            directions = self.get_neighbours(r, c)

            keys = list(directions.keys())
            for i in range(0, len(directions) - 1, 2):
                positive_direction = directions[keys[i]]
                negative_direction = directions[keys[i + 1]]
                score = 0
                for neighbour in positive_direction:
                    if neighbour == cell_to_check:
                        score += 1
                    else:
                        break
                for neighbour in negative_direction:
                    if neighbour == cell_to_check:
                        score += 1
                    else:
                        break

                if(score >= self.win_span - 1):
                   ## print(keys[i],"->" ,positive_direction)
                   ## print(keys[i+1], "->", negative_direction)

                    self.game_over = True
                    for player in self.players:
                        if int(player) == int(cell_to_check):
                            self.winner = player
                            return player

        if len(self.get_actions()) == 0:
            return 0
        return -1