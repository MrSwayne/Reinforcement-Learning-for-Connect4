import numpy as np

class TicBoard():

    def __init__(self, players):
        self.rows = 3
        self.cols = 3
        self.players = players
        self.board = np.zeros([self.rows, self.cols])
        self.turn = 0

    def get_player_turn(self):
        return (self.players[(self.turn % len(self.players))]);

    def get_actions(self):
        actions = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r,c] == 0:
                    actions.append((r,c))
        return actions

    def place(self, *args):
        r = args[0]
        c = args[1]

        if self.board[r,c] == 0:
            self.board[r,c] = int(self.get_player_turn())
            self.turn += 1
            return True
        return False



    def get_state(self, player):
        string = ""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r,c] == int(player):
                    string += "1"
                elif self.board[r,c] in self.players:
                    string += "2"
                else:
                    string += "0"
        return string








