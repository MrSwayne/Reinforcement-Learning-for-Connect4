import numpy as np
import matplotlib.pyplot as plt
import copy
class Board():

    # rows
    #     #@params
    #     #= # of rows (default 6)
    # cols = # of cols (default 7)
    # win_span = # in a row for a win (default 4 because it's connect4 lol)
    #

    def __init__(self, players = [], rows=6, cols=7, win_span = 4):
        self.rows = rows
        self.cols = cols
       # self.init_board[self.init_board == 0] = -1
        self.board = self.init_state()
        self.players = players
        self.num_players = len(players)
        self.win_span = win_span

        self.col_index={}
        for c in range(cols):
            self.col_index[c] = 0

    def init_state(self):
        self.turn = 0
        self.winner = -1
        self.game_over = False
        self.last_move = {"R":-1, "C":-1}
        self.moves = []
        return np.zeros([self.rows, self.cols])  ##.astype(str)

    def get_state(self):
        return self.board

    def placeSequence(self, list):
        bools = []
        for choice in list:
            if self.place(choice):
                bools.append(True)
            else:
                bools.append(False)
        return bools

    def print(self):
        for r in range(self.rows):
            print(r, "|", end = " ")
            for c in range(self.cols):
                print(int(self.board[r,c]), end=" ")
            print()
        print("-" * (self.cols + self.cols - 1 + 4) )

        print("  ", end = "  ")
        for c in range(self.cols):
            print(c, end = " ")
        print()

    def clone(self):

        newBoard = Board(self.players, self.rows, self.cols, self.win_span)
        newBoard.board = np.copy(self.board)
        newBoard.turn = self.turn
        newBoard.game_over = self.game_over
        newBoard.moves = copy.copy(self.moves)
        newBoard.last_move = copy.copy(self.last_move)
        return newBoard

    def get(self, row, col):
        if row >= 0 and row < self.rows:
            if col >= 0 and col < self.cols:
                return self.board[row, col]

        return -1


    def place(self, col):
        if 0 <= col < self.cols:
            if int(self.check_win(True)) > 0:
                return False

            for r in range(self.rows - 1, -1, -1):
                if self.board[r,col] == 0:
                    self.board[r,col] = int(self.get_player_turn());
                    self.turn += 1
                    self.moves.append(col)
                    self.last_move["R"] = r
                    self.last_move["C"] = col
                    return True
        return False

    def get_player_turn(self):
      #  print(self.players[(self.turn % self.num_players)])
        return (self.players[(self.turn % self.num_players)]);


    def get_state(self):
        return self.board

    def get_actions(self):
        available = []

        for c in range(self.cols):
            if self.board[0, c] == 0:
                available.append(c)

        if len(available) == 0:
            self.game_over = True

        return available

    def get_neighbours(self, r, c):
        if c >= 0 and c < self.cols and r >= 0 and r < self.rows:

            cell_to_check = self.get(r, c)

            if cell_to_check > 0:
                #   print("checking", c, " ", r, " [", cell_to_check, "]", end = "\t")
                ##get left

                left = 0
                for col in range(c - 1, c - self.win_span + 1, -1):
                    neighbour_cell = self.get(r, col)
                    if neighbour_cell == cell_to_check:
                        left += 1
                    else:
                        break
                ##get right


                right = 0
                for col in range(c + 1, c + self.win_span, 1):

                    neighbour_cell = self.get(r, col)
                    if neighbour_cell == cell_to_check:
                        right += 1
                    else:
                        break

                ##get top
                top = 0
                for row in range(r - 1, r - self.win_span + 1, -1):
                    neighbour_cell = self.get(row, c)
                    if neighbour_cell == cell_to_check:
                        top += 1
                    else:
                        break

                ##get bottom
                bottom = 0
                for row in range(r + 1, r + self.win_span, 1):
                    neighbour_cell = self.get(row, c)
                    if neighbour_cell == cell_to_check:
                        bottom += 1
                    else:
                        break

                ##get top_left
                top_left = 0

                for i in range(self.win_span - 1):
                    row = r - (i + 1)
                    col = c - (i + 1)
                    neighbour_cell = self.get(row, col)
                    if neighbour_cell == cell_to_check:
                        top_left += 1
                    else:
                        break

                ##get bottom_right

                bottom_right = 0
                for i in range(self.win_span):
                    row = r + (i + 1)
                    col = c + (i + 1)
                    neighbour_cell = self.get(row, col)
                    if neighbour_cell == cell_to_check:
                        bottom_right += 1
                    else:
                        break

                ##get bottom_left

                bottom_left = 0
                temp_row = r + 1
                temp_col = c - 1
                for i in range(self.win_span - 1):
                    neighbour_cell = self.get(temp_row, temp_col)
                    if neighbour_cell == cell_to_check:
                        bottom_left += 1
                    else:
                        break
                    temp_row += 1
                    temp_col -= 1

                ##get top_right
                temp_row = r - 1
                temp_col = c + 1

                top_right = 0
                for i in range(self.win_span - 1):
                    neighbour_cell = self.get(temp_row, temp_col)
                    if neighbour_cell == cell_to_check:
                        top_right += 1
                    else:
                        break
                    temp_row -= 1
                    temp_col += 1

                directions = [(left, right), (top, bottom), (top_left, bottom_right), (bottom_left, top_right)]
                return directions
        return [(0, 0)]


    def check_win(self, step = False):
        cells_to_check = []

        if step:
            R = self.last_move["R"]
            C =self.last_move["C"]
            cells_to_check.append((self.get(R,C), R, C))
        else:
            for r in range(self.rows):
                for c in range(self.cols):
                    cells_to_check.append((self.get(r,c), r, c))

        for cell_to_check_tuple in cells_to_check:
            cell_to_check = cell_to_check_tuple[0]
            r = cell_to_check_tuple[1]
            c = cell_to_check_tuple[2]

            directions = self.get_neighbours(r, c)
          #  print("{0}, {1} has neighbours :  {2}".format( r, c, directions))
            for directionTuple in directions:
                if (directionTuple[0] + directionTuple[1]) >= self.win_span - 1:
                    self.game_over = True
                    for player in self.players:
                        if int(player) == int(cell_to_check):
                            return player

        if len(self.get_actions()) == 0:
            return 0
        return -1