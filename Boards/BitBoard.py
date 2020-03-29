import numpy as np
import matplotlib.pyplot as plt
import sys
import time
from abc import abstractmethod
import copy


class BitBoard():

    # rows
    #     #@params
    #     #= # of rows (default 6)
    # cols = # of cols (default 7)
    # win_span = # in a row for a win (default 4 because it's connect4 lol)
    #

    def __init__(self, players, rows, cols, win_span):
        self.rows = rows
        self.cols = cols
        self.players = players
        self.win_span = win_span
        self.turn = 0
        self.game_over = False
        self.moves = []
        self.winner = -1
        self.last_action = None

        self.boards = {}
        for p in self.players:
            self.boards[p] = 0

    def num_moves(self):
        return len(self.moves)


    def undo(self):
        self.moves.pop()
        if len(self.moves) == 0:
            self.last_action = None
        else:
            self.last_action = self.moves[len(self.moves) - 1]
        self.turn -= 1

        if self.game_over:
            self.game_over = False

    def get_boards(self):
        return self.boards

    def get_mask(self):
        state = 0
        for p in self.players:
            state ^= self.boards[p]
        return state

    def get_state(self, player=None):

        states = []
        for player, player_board in self.boards.items():
            states.append(player_board)

        states.append(int(self.turn) % len(self.players))
        return tuple(states)

    def reset(self):
        for p in self.players:
            self.boards[p] = 0

        self.turn = 0
        self.last_action = None
        self.game_over = False
        self.moves = []


    def to_bit_string(self, player=None):
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
                    index = self.get_index(r, c)
                    if (b >> index) & 1 == 1:
                        to_be_printed = int(p)
                print(to_be_printed, end=" ")
            print()
        print()

    def set_state(self, player, b):
        if player in self.boards:
            self.boards[player] = b


    def get(self, row, col):

        if row >= self.rows or row < 0 or col >= self.cols or col < 0:
            return -1

        index = self.get_index(row, col)
        for p, b in self.boards.items():
            if (b >> index) & 1 == 1:
                return p
        return 0

    def set_bit(self, player, bit, turn_on=True):

        if turn_on:
            self.boards[player] |= (1 << bit)
        else:
            self.boards[player] &= ~(1 << (bit))

    def get_last_move(self):
        if len(self.moves) > 0:
            return self.moves[len(self.moves) - 1]
        return None

    def get_index(self, row, col):
        return int((self.rows - row) + (col * (self.cols - (self.cols - self.rows - 1))) - 1)

    def get_row_col(self, index):
        pass


    def place_sequence(self, cols):
        bools = []
        for col in cols:
            bools.append(self.place(col))
        return bools


    def place(self, action):
        self.turn += 1
        self.moves.append(action)
        self.last_action = action
        self.check_win()
        return True


    def get_player_turn(self, prev=False):
        turn = self.turn
        if prev:
            turn -= 1

        return self.players[(turn % len(self.players))];

    def get_players(self):
        return self.players

    @abstractmethod
    def get_actions(self):
        pass

    ##Bitboard black magic
    def check_win(self):
        ##Vertical |, horizontal -, diagonal \, diagonal /
        directions = [1, self.rows + 1, self.rows, self.rows + 2]

        # Only need to worry about the player who placed last, assuming that check_win is called after every placement
        player_to_check = self.get_player_turn(prev=True)

        board = self.boards[player_to_check]

        for direction in directions:
            m = board
          #  print(direction)
            # Loop for however many discs we need in a row
            for i in range(self.win_span):
                # Shift the board i amount of columns/rows
               # print(bin(m), " ", bin(board >> (direction * i)))
                m = m & (board >> (direction * i))

            # If after the board is shifted and logical AND'ed together >= 1, that means there is 4 in a row
            if m:
                self.game_over = True
                self.winner = player_to_check
                return player_to_check

        # If there are no actions, then it's a draw
        if (len(self.get_actions()) == 0):
            self.game_over = True
            self.winner = 0
            return 0
        # Game is on going
        self.winner = -1
        self.game_over = False
        return -1
