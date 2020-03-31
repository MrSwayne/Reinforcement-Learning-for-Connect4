from Boards.BitBoard import *

class ConnectBoard(BitBoard):

    def __init__(self, players, rows=6, cols=7, win_span=4):
        super().__init__(players=players, rows=rows, cols=cols, win_span=win_span)
        self.high = []
        for i in range(self.cols):
            self.high.append(self.rows)
        self.num_bandits = len(self.get_actions())

    def undo(self):
        last_col = self.moves[len(self.moves) - 1]
        last_row = self.high[last_col]
        index = self.get_index(col=last_col, row=last_row)
        self.high[last_col] += 1
        self.set_bit(self.get_player_turn(prev=True), index, turn_on=False)
        super().undo()

    def reset(self):
        self.high = []
        for i in range(self.cols):
            self.high.append(self.rows)
        super().reset()


    def __deepcopy__(self, memodict={}):
        newBoard = ConnectBoard(self.players, self.rows, self.cols, self.win_span)
        newBoard.high = copy.deepcopy(self.high)
        for p, b in self.boards.items():
            newBoard.set_state(p, b)
        newBoard.turn = self.turn
        newBoard.game_over = self.game_over
        newBoard.moves = copy.deepcopy(self.moves)
        newBoard.winner = self.winner
        return newBoard


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

    def place(self, action):
        if not self.game_over:

            if type(action) == tuple:
                action = action[1]

            if self.high[action] > 0:
                row = self.high[action] - 1
                bit = self.get_index(row=row, col=action)
                self.set_bit(self.get_player_turn(), bit)
                self.high[action] -= 1
                super().place(action)
                return True
        return False