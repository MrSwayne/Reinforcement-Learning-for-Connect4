from abc import abstractmethod
import numpy as np
import copy
class Board():

    def __init__(self, players = [], rows = 0, cols = 0):
        self.players = players
        self.rows = rows
        self.cols = cols

        self.board = np.zeros([self.rows, self.cols])
        self.turn = 0
        self.winner = None
        self.game_over = False
        self.moves = []

    @abstractmethod
    def get_state(self, player):
        pass


    def place_sequence(self, list):
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
                if int(self.board[r,c]) == 0:
                    print(" ", end = " ")
                else:
                    print(int(self.board[r,c]), end=" ")
            print()
        print("-" * (self.cols + self.cols - 1 + 4) )

        print("  ", end = "  ")
        for c in range(self.cols):
            print(c, end = " ")
        print()

    @abstractmethod
    def place(self, *action):
        pass

    def get_player_turn(self):
        return (self.players[(self.turn % len(self.players))])

    def get_players(self):
        return self.players

    @abstractmethod
    def get_actions(self):
        pass

    @abstractmethod
    def get_last_action(self):
        pass

    @abstractmethod
    def get_last_move(self):
        if len(self.moves) == 0:
            return None
        else:
            return self.moves[len(self.moves) - 1]

    @abstractmethod
    def check_win(self):
        pass


    def get_c(self, row, col):
        if row >= 0 and row < self.rows:
            if col >= 0 and col < self.cols:
                return self.board[row, col]

        return -1

    def get(self, row, col):
        if row >= 0 and row < self.rows:
            if col >= 0 and col < self.cols:
                for p in self.players:
                    if int(p) == self.board[row,col]:
                        return p
        return -1