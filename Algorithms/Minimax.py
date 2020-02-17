import copy
from threading import *
from queue import Queue

from Algorithms.Algorithm import *


class AlphaBeta_h(Algorithm):


    def get_values(self):
        return self.scores

    def __init__(self, max_depth = 4):
        super().__init__()
        self.max = None
        self.min = None
        self.max_depth = max_depth
        self.scores = {}

    def get_move(self, state):
        self.max = state.get_player_turn()
        self.min = state.get_player_turn(prev=True)

        max_score = float("-inf")
        best_action = None

        for action in state.get_actions():

            _state = copy.deepcopy(state)
            _state.place(action)
            score = self.minimax(_state)
            self.scores[action] = score
            if score >= max_score:
                best_action = action
                max_score = score
        return best_action

    def minimax(self, state, alpha=float("-inf"), beta=float("inf"), depth = 0):
        if state.game_over:
            winner = state.winner

            if winner == self.max:
                return 10
            elif winner == self.min:
                return -10
            else:
                return 0

        if depth == self.max_depth:
            return self.heuristic(state, state.get_player_turn(), state.win_span)

        max_score = float("-inf")
        min_score = float("inf")
        for action in state.get_actions():
            score = 0
            _state = copy.deepcopy(state)
            _state.place(action)

            score += self.minimax(_state, alpha, beta, depth + 1)

            max_score = max(max_score, score)
            if state.get_player_turn() == self.max:
                alpha = max(alpha, max_score)

            min_score = min(min_score, score)
            if state.get_player_turn() == self.min:
                beta = min(beta, min_score)

            if beta <= alpha:
                break

        if(state.get_player_turn() == self.max):
            return max_score
        else:
            return min_score

    def heuristic(self, state, player, win_span):

        steps = {}
        steps["leftDiagonal"] = [(-1,-1), (1,1)]
        steps["rightDiagonal"] = [(1,-1), (-1,1)]
        steps["left"] = [(-1,0), (1,0)]
        steps["up"] = [(0,-1), (0,1)]

        for r in range(state.rows):
            for c in range(state.cols):
                pass


    def check_win(self, state, player, win_span):
        ##Vertical |, horizontal -, diagonal \, diagonal /
        directions = [1,state.rows + 1, state.rows, state.rows + 2]

        # Only need to worry about the player who placed last, assuming that check_win is called after every placement
        board = state.boards[player]

        for direction in directions:
            m = board

            # Loop for however many discs we need in a row
            for i in range(win_span):
                # Shift the board i amount of columns/rows
                m = m & (board >> (direction * i))

            # If after the board is shifted and logical AND'ed together >= 1, that means there is 4 in a row
            if m:
                return True

        # If there are no actions, then it's a draw
        if (len(state.get_actions()) == 0):
            return False

        # Game is on going
        return False



class AlphaBeta(Algorithm):


    def get_values(self):
        return self.scores

    def __init__(self, max_depth = 4):
        super().__init__()
        self.max = None
        self.min = None
        self.max_depth = max_depth
        self.scores = {}

    def get_move(self, state):
        self.max = state.get_player_turn()
        self.min = state.get_player_turn(prev=True)

        max_score = float("-inf")
        best_action = None

        for action in state.get_actions():

            _state = copy.deepcopy(state)
            _state.place(action)
            score = self.minimax(_state)
            self.scores[action] = score
            if score >= max_score:
                best_action = action
                max_score = score
        return best_action

    def minimax(self, state, alpha=float("-inf"), beta=float("inf"), depth = 0):
        if state.game_over:
            winner = state.winner

            if winner == self.max:
                return 10
            elif winner == self.min:
                return -10
            else:
                return 0

        if depth == self.max_depth:
            return self.heuristic(state, state.get_player_turn(), state.win_span)

        max_score = float("-inf")
        min_score = float("inf")
        for action in state.get_actions():
            score = 0
            _state = copy.deepcopy(state)
            _state.place(action)

            score += self.minimax(_state, alpha, beta, depth + 1)

            max_score = max(max_score, score)
            if state.get_player_turn() == self.max:
                alpha = max(alpha, max_score)

            min_score = min(min_score, score)
            if state.get_player_turn() == self.min:
                beta = min(beta, min_score)

            if beta <= alpha:
                break

        if(state.get_player_turn() == self.max):
            return max_score
        else:
            return min_score

    def heuristic(self, state, player, win_span):

        if win_span <= 1:
            return 0
        score = 0

        for p in state.players:
            if(self.check_win(state, p, win_span)):
                if(p == player):
                    score += win_span
                else:
                    score -= win_span

        score += self.heuristic(state, player, win_span - 1)
        return score

    def check_win(self, state, player, win_span):
        ##Vertical |, horizontal -, diagonal \, diagonal /
        directions = [1,state.rows + 1, state.rows, state.rows + 2]

        # Only need to worry about the player who placed last, assuming that check_win is called after every placement
        board = state.boards[player]

        for direction in directions:
            m = board

            # Loop for however many discs we need in a row
            for i in range(win_span):
                # Shift the board i amount of columns/rows
                m = m & (board >> (direction * i))

            # If after the board is shifted and logical AND'ed together >= 1, that means there is 4 in a row
            if m:
                return True

        # If there are no actions, then it's a draw
        if (len(state.get_actions()) == 0):
            return False

        # Game is on going
        return False


class Minimax(Algorithm):


    def get_values(self):
        return self.scores

    def __init__(self, max_depth = 4):
        super().__init__()
        self.max = None
        self.min = None
        self.max_depth = max_depth
        self.scores = {}

    def get_move(self, state):
        self.max = state.get_player_turn()
        self.min = state.get_player_turn(prev=True)

        max_score = float("-inf")
        best_action = None

        for action in state.get_actions():

            _state = copy.deepcopy(state)
            _state.place(action)
            score = self.minimax(_state)
            self.scores[action] = score
            if score >= max_score:
                best_action = action
                max_score = score
        return best_action

    def minimax(self, state, depth = 0):
        if state.game_over:
            winner = state.winner

            if winner == self.max:
                return 10
            elif winner == self.min:
                return -10
            else:
                return 0

        if depth == self.max_depth:
            return self.heuristic(state, state.get_player_turn(), state.win_span)

        max_score = float("-inf")
        min_score = float("inf")
        for action in state.get_actions():
            score = 0
            _state = copy.deepcopy(state)
            _state.place(action)

            score += self.minimax(_state, depth + 1)

            if score >= max_score:
                max_score = score
            if score <= min_score:
                min_score = score
          #  print(max_score, "..", min_score, "->", score)

        if(state.get_player_turn() == self.max):
            return max_score
        else:
            return min_score

    def heuristic(self, state, player, win_span):

        if win_span <= 1:
            return 0
        score = 0

        for p in state.players:
            if(self.check_win(state, p, win_span)):
                if(p == player):
                    score += win_span
                else:
                    score -= win_span

        score += self.heuristic(state, player, win_span - 1)
        return score

    def check_win(self, state, player, win_span):
        ##Vertical |, horizontal -, diagonal \, diagonal /
        directions = [1,state.rows + 1, state.rows, state.rows + 2]

        # Only need to worry about the player who placed last, assuming that check_win is called after every placement
        board = state.boards[player]

        for direction in directions:
            m = board

            # Loop for however many discs we need in a row
            for i in range(win_span):
                # Shift the board i amount of columns/rows
                m = m & (board >> (direction * i))

            # If after the board is shifted and logical AND'ed together >= 1, that means there is 4 in a row
            if m:
                return True

        # If there are no actions, then it's a draw
        if (len(state.get_actions()) == 0):
            return False

        # Game is on going
        return False



class Minimax_t(Algorithm):

    def __init__(self, max_depth = 4):
        super().__init__()
        self.max = None
        self.min = None
        self.max_depth = max_depth
        self.scores = {}

    def get_values(self):
        return self.scores

    def get_move(self, state):
        self.max = state.get_player_turn()
        self.min = state.get_player_turn(prev=True)

        self.scores = {}

        state_actions = state.get_actions()

        threads = []
        queue = Queue()
        for action in state_actions:
            _state = copy.deepcopy(state)
            _state.place(action)

            t = Thread(target=lambda q, s: q.put((self.minimax(s, 0), action)), args=(queue, _state))
            t.start()
            threads.append(t)

        count = 0

        max_score = float("-inf")
        best_action = None
        while count < len(state_actions):
            if queue.not_empty:
                (score,action) = queue.get()

                if score >= max_score:
                    max_score = score
                    best_action = action
                count += 1
        return best_action

    def minimax(self, state, depth = 0):
        if state.game_over:
            winner = state.winner

            if winner == self.max:
                return 10
            elif winner == self.min:
                return -10
            else:
                return 0

        if depth == self.max_depth:
            return self.heuristic(state, state.get_player_turn(), state.win_span)

        max_score = float("-inf")
        min_score = float("inf")

        for action in state.get_actions():
            score = 0
            _state = copy.deepcopy(state)
            _state.place(action)
            score += self.minimax(_state, depth + 1)
            if score >= max_score:
                max_score = score
            if score <= min_score:
                min_score = score

        if(state.get_player_turn() == self.max):
            return max_score
        else:
            return min_score

    def heuristic(self, state, player, win_span):

        if win_span <= 1:
            return 0
        score = 0

        for p in state.players:
            if(self.check_win(state, p, win_span)):
                if(p == player):
                    score += win_span
                else:
                    score -= win_span

        score += self.heuristic(state, player, win_span - 1)
        return score

    def check_win(self, state, player, win_span):
        ##Vertical |, horizontal -, diagonal \, diagonal /
        directions = [1,state.rows + 1, state.rows, state.rows + 2]

        # Only need to worry about the player who placed last, assuming that check_win is called after every placement
        board = state.boards[player]

        for direction in directions:
            m = board

            # Loop for however many discs we need in a row
            for i in range(win_span):
                # Shift the board i amount of columns/rows
                m = m & (board >> (direction * i))

            # If after the board is shifted and logical AND'ed together >= 1, that means there is 4 in a row
            if m:
                return True

        # If there are no actions, then it's a draw
        if (len(state.get_actions()) == 0):
            return False

        # Game is on going
        return False
