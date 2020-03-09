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

        best_children = []
        for action in state.get_actions():

            _state = copy.deepcopy(state)
            _state.place(action)
            score = self.minimax(_state)
            self.scores[action] = score
            if score > max_score:
                best_children = []
                max_score = score
            if score >= max_score:
                best_children.append(action)
        return random.choice(best_children)

    def minimax(self, state, alpha=float("-inf"), beta=float("inf"), depth=0):

        if depth == self.max_depth:
            return self.heuristic(state, state.get_player_turn(), state.win_span)

        if state.game_over:
            winner = state.winner

            if winner == self.max:
                return 100 - depth
            elif winner == self.min:
                return -100 + depth
            else:
                return 0

        if state.get_player_turn() == self.max:
            val = float("-inf")
            for action in state.get_actions():
                _state = copy.deepcopy(state)
                _state.place(action)
                val = max(val, self.minimax(_state, alpha, beta, depth + 1))

                alpha = max(alpha, val)

                if alpha >= beta:
                    break
            return val

        else:
            val = float("inf")
            for action in state.get_actions():
                _state = copy.deepcopy(state)
                _state.place(action)

                val = min(val, self.minimax(_state, alpha, beta, depth + 1))

                beta = min(beta, val)
                if alpha >= beta:
                    break
            return val

    def heuristic(self, state, player, win_span):
        total_score = 0

        for r in range(state.rows):
            for c in range(state.cols):
                cell = state.get(r, c)
                if cell is not 0:

                    neighbours = self.get_neighbours(state, r, c, win_span)

                    score = 1
                    for i in range(0, len(neighbours) - 1, 2):
                        dirs = [neighbours[i], neighbours[i + 1]]
                        for dir in dirs:
                            for neighbour in dir:
                                if neighbour == 0:
                                    score += 0.2
                                if neighbour == cell:
                                    score += 1
                                else:
                                    break
                    if int(cell) == int(player):
                        total_score += score
                    else:
                        total_score -= score

        return total_score

    def check_win(self, state, player, win_span):
        ##Vertical |, horizontal -, diagonal \, diagonal /
        directions = [1, state.rows + 1, state.rows, state.rows + 2]

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

    def get_neighbours(self, board, r, c, win_span):
        map = {"LEFT": [], "RIGHT": [], "UP": [], "DOWN": [], "UP_LEFT": [], "DOWN_RIGHT": [], "UP_RIGHT": [],
               "DOWN_LEFT": []}

        map = []
        if c >= 0 and c < board.cols and r >= 0 and r < board.rows:
            cell = board.get(r, c)

            if cell is not 0:

                list = []
                for col in range(c - 1, c - win_span, -1):
                    neighbour_cell = board.get(r, col)
                    list.append(neighbour_cell)
                map.append(list)
                ##get right

                list = []
                for col in range(c + 1, c + win_span, 1):
                    neighbour_cell = board.get(r, col)

                    list.append(neighbour_cell)
                map.append(list)
                ##get up

                list = []
                for row in range(r - 1, r - win_span, -1):
                    neighbour_cell = board.get(row, c)

                    list.append(neighbour_cell)
                map.append(list)
                ##get down

                list = []
                for row in range(r + 1, r + win_span, 1):
                    neighbour_cell = board.get(row, c)

                    list.append(neighbour_cell)

                    ##get up_left
                map.append(list)

                list = []
                for i in range(win_span - 1):
                    row = r - (i + 1)
                    col = c - (i + 1)
                    neighbour_cell = board.get(row, col)
                    list.append(neighbour_cell)
                map.append(list)

                ##get down_right
                list = []
                for i in range(win_span - 1):
                    row = r + (i + 1)
                    col = c + (i + 1)
                    neighbour_cell = board.get(row, col)
                    list.append(neighbour_cell)
                map.append(list)
                ##get bottom_left

                temp_row = r + 1
                temp_col = c - 1
                list = []
                for i in range(win_span):
                    neighbour_cell = board.get(temp_row, temp_col)

                    list.append(neighbour_cell)
                    temp_row += 1
                    temp_col -= 1

                ##get up right
                temp_row = r - 1
                temp_col = c + 1
                map.append(list)
                list = []
                for i in range(win_span - 1):
                    neighbour_cell = board.get(temp_row, temp_col)

                    list.append(neighbour_cell)
                    temp_row -= 1
                    temp_col += 1
                map.append(list)
        return map


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

        best_children = []
        for action in state.get_actions():
            _state = copy.deepcopy(state)
            _state.place(action)
            score = self.minimax(_state)
            self.scores[action] = score
            if score > max_score:
                best_children = []
                max_score = score
            if score >= max_score:
                best_children.append(action)
        return random.choice(best_children)

    def minimax(self, state, alpha=float("-inf"), beta=float("inf"), depth = 0):
        if state.game_over:
            winner = state.winner
            if winner == self.max:
                return 100 - depth
            elif winner == self.min:
                return -100 + depth
            else:
                return 0

        if depth == self.max_depth:
            return self.heuristic(state, state.get_player_turn(), state.win_span)

        if state.get_player_turn() == self.max:
            val = float("-inf")
            for action in state.get_actions():
                _state = copy.deepcopy(state)
                _state.place(action)
                val = max(val, self.minimax(_state, alpha, beta, depth + 1))

                alpha = max(alpha, val)

                if alpha >= beta:
                    break
            return val

        else:
            val = float("inf")
            for action in state.get_actions():
                _state = copy.deepcopy(state)
                _state.place(action)

                val = min(val, self.minimax(_state, alpha, beta, depth+1))

                beta = min(beta, val)
                if alpha >= beta:
                    break
            return val

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
