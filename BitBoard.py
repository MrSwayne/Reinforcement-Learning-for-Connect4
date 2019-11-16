import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import copy
class BitBoard():

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
        self.win_span = win_span
        self.turn = 0
        self.game_over = False
        self.moves = []

        self.high = []
        for i in range(self.cols):
            self.high.append(self.rows)

        self.boards = {}
        for p in self.players:
            self.boards[p] = 0

    def num_moves(self):
        return len(self.moves)

    #todo
    def undo(self):
        last_col = self.moves[len(self.moves) - 1]
        last_row = self.high[last_col]
        index = self.get_index(col=last_col, row=last_row)


        self.set_bit(self.get_player_turn(prev=True), index, turn_on=False)
        self.moves.pop()
        self.turn -= 1
        self.high[last_col] += 1
        if self.game_over:
            self.game_over = False

    def get_boards(self):
        return self.boards

    def get_state(self, player = None):
        state = None

        if player is not None:
            return self.boards[player]

        for player, player_board in self.boards.items():
            if state is None:
                state = player_board
            else:
                state ^= player_board
        return state

    def to_bit_string(self, player = None):
        string = 0
        if player is None:
            string = self.get_state()
        else:
            string = self.get_state(player)

        return "{0:b}".format(string)

    def print(self):
        for r in range(self.rows):
            for c in range(self.cols):
                to_be_printed = 0
                for p, b in self.boards.items():
                    index = self.get_index(r,c)
                    if (b >> index) & 1 == 1:
                        to_be_printed = int(p)
                print(to_be_printed, end = " ")
            print()
        print()

    def __set_state(self, player, b):
        if player in self.boards:
            self.boards[player] = b

    def __deepcopy__(self, memodict={}):
        newBoard = BitBoard(self.players, self.rows, self.cols, self.win_span)

        for p, b in self.boards.items():
            newBoard.__set_state(p, b)
        newBoard.high = copy.deepcopy(self.high)
        newBoard.turn = self.turn
        newBoard.game_over = self.game_over
        newBoard.moves = copy.deepcopy(self.moves)
        return newBoard

    def get(self, row, col):
        index = self.get_index(row, col)
        for p, b in self.boards.items():
            if (b >> index) & 1 == 1:
                return p
        return 0


    def set_bit(self, player, bit, turn_on=True):
        if turn_on:
            self.boards[player] |= (1 << bit)
        else:
            self.boards[player] &= ~(1 << (bit - 1))

    def get_last_move(self):
        if len(self.moves) > 0:
            return self.moves[len(self.moves) - 1]
        return None

    def get_index(self, row, col):
        return (self.rows - row) + (col * (self.cols - (self.cols - self.rows -1))) - 1

    def place_sequence(self, *cols):
        bools = []
        for col in cols:
            bools.append(self.place(col))
        return bools


    def place(self, col):

        if not self.game_over:
            if self.high[col] > 0:
                row = self.high[col] - 1
                bit = self.get_index(row=row, col=col)

                self.set_bit(self.get_player_turn(), bit)
                self.high[col] -= 1
                self.turn += 1
                self.moves.append(col)
                self.check_win()
                return True
        return False

    def get_player_turn(self, prev=False):
        turn = self.turn
        if prev:
            turn -= 1

        return self.players[(turn % len(self.players))];


    def get_players(self):
        return self.players

    def get_actions(self):
        if self.game_over:
            return []

        available = []

        for c in range(self.cols):
            if self.high[c] > 0:
                available.append(c)

        if len(available) == 0:
            self.game_over = True

        return available

    ##Bitboard black magic
    def check_win(self):
        ##Vertical |, horizontal -, diagonal \, diagonal /
        directions = [1, self.rows + 1, self.rows, self.rows + 2]

        player_to_check = self.get_player_turn(prev=True)
        board = self.boards[player_to_check]

        for direction in directions:
            m = board
            for in_a_row in range(self.win_span):
                m = m & (board >> (direction * in_a_row))
            if m:
                self.game_over = True
                if player_to_check is None:
                    return True
                return player_to_check

        if(len(self.get_actions()) == 0):
            self.game_over = True
            return 0
        return -1