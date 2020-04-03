from Boards.BitBoard import *
class TicBoard(BitBoard):
    def __init__(self, players, rows=3, cols=3, win_span=3):
        super().__init__(players=players, rows=rows, cols=cols, win_span=win_span)
        self.num_bandits = len(self.get_actions())

    def undo(self):
        if len(self.moves[len(self.moves) - 1]) == 0:
            action = None
        else:
            action = self.moves[len(self.moves) - 1]
        last_row = action[0]
        last_col = action[1]

        index = self.get_index(col=last_col, row=last_row)
        self.set_bit(self.get_player_turn(prev=True), index, turn_on=False)
        super().undo()

    def place(self,action):
        if not self.game_over:
            row = action[0]
            col = action[1]
            bit = self.get_index(row=row, col=col)
            self.set_bit(self.get_player_turn(), bit)
            super().place(action)
        return False

    def __deepcopy__(self, memodict={}):
        newBoard = TicBoard(self.players, self.rows, self.cols, self.win_span)

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
        for r in range(self.rows):
            for c in range(self.cols):
                if self.get(r, c) == 0:
                    available.append((r,c))

        if len(available) == 0:
            self.game_over = True

        return available