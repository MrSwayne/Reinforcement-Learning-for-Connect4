import numpy as np
import matplotlib.pyplot as plt
import bitstring as bt
import time
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

        self.players = players
        self.num_players = len(players)
        self.win_span = win_span
        self.init_state()

    #todo
    def undo(self):
        last_col = self.moves[len(self.moves) - 1]
        last_row = self.high[last_col]
        index = self.get_index(col=last_col, row=last_row)
        return index



    def init_state(self):
        self.turn = 0
        self.game_over = False
        self.moves = []

        self.high = []

        string = ""
        for r in range(self.rows + 1):
            for c in range(self.cols):
                if r == 0:
                    string += "0"
                    self.high.append(0)
                else:
                    string += "0"

        boards = []
        prev_boards = []

        for p in self.players:
            boards.append( bt.BitArray(bin=string))
            prev_boards.append(bt.BitArray(bin=string))

        self.prev_boards = prev_boards
        self.boards = boards


    def get_boards(self):
        return self.boards

    def get_state(self):
        state = None
        for player_board in self.boards:
            if state is None:
                state = player_board
            else:
                state ^= player_board
        return state.bin

    def placeSequence(self, list):
        bools = []
        for choice in list:
            if self.place(choice):
                bools.append(True)
            else:
                bools.append(False)
        return bools

    def print(self):

        for r in range(self.rows - 1, -1, -1 ):
            for c in range(0, self.cols):

                #print(self.get_index(c, r), end="\t")
                to_be_printed = 0
                for j in range(len(self.boards)):
                    board = self.boards[j]
                    if board[self.get_index(r,c)] == True:
                        to_be_printed = j + 1
                print(to_be_printed, end = " ")
            print()
        print()

    def print_player(self, player):
        for i in range(len(self.players)):
            if self.players[i] == player:
                board = self.boards[i]
                for r in range(self.rows - 1, -1, -1):
                    for c in range(0, self.cols):

                        # print(self.get_index(c, r), end="\t")
                        to_be_printed = 0

                        if board[self.get_index(r, c)] == True:
                            to_be_printed = 1
                        print(to_be_printed, end=" ")
                    print()


    def __deepcopy__(self, memodict={}):
        newBoard = Board(self.players, self.rows, self.cols, self.win_span)

        for i in range(len(self.boards)):
            newBoard.boards[i] = copy.deepcopy(self.boards[i])
        newBoard.turn = self.turn
        newBoard.game_over = self.game_over
        newBoard.moves = copy.deepcopy(self.moves)
        return newBoard

    def get_index(self, col, row):
        if row >= 0 and row <= self.rows:
            if col >= 0 and col <= self.cols:

                index = (row)  * self.cols + col
                return index
                #return self.board[row, col]
        return -1

    def get(self, row, col):
        index = self.get_index(row, col)
        if index >= 0:
            for i in range(len(self.boards)):
                if self.boards[i][index]:
                    return self.players[i]
            return 0
        return index

    def __set(self, row, col, player, value = True):
        for i in range(len(self.players)):
            if self.players[i] == player:

                self.boards[i][self.get_index(row, col)] = value
                return True
        return False
               # self.board[self.get_index(row, col)] = "0b1"

    def get_last_move(self):
        if len(self.moves) > 0:
            return self.moves[len(self.moves) - 1]
        return None

    def place(self, col):
        self.check_win()

        if not self.game_over:
            if self.high[col] < self.rows:
                if self.__set(row = self.high[col], col = col, player = self.get_player_turn()):
                    self.high[col] += 1
                    self.turn += 1
                    self.moves.append(col)
                    return True
        return False

    def get_player_turn(self, prev=False):
        turn = self.turn
        if prev:
            turn -= 1

        return (self.players[(turn % self.num_players)]);


    def get_players(self):
        return self.players

    def get_actions(self):
        if self.game_over == True:
            return []

        available = []

        for c in range(self.cols):
            if self.high[c] < self.rows:
                available.append(c)

        if len(available) == 0:
            self.game_over = True

        return available

    ##Bitboard black magic
    def check_win(self):
        ##Vertical |, horizontal -, diagonal \, diagonal /
        directions = [1, 7, 6, 8]
        for i in range(len(self.players)):
            board = self.boards[i]
            for direction in directions:
                m = board
                for in_a_row in range(self.win_span):
                    m = m & (board >> (direction * in_a_row))
                if m:
                    self.game_over = True
                    return self.players[i]

        if(len(self.get_actions()) == 0):
            self.game_over = True
            return 0

        return -1