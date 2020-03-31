import copy
from threading import *
from queue import Queue
from Core import LOGGER
from Algorithms.Algorithm import *

logger = LOGGER.attach(__name__)

class AlphaBeta_V2(Algorithm):
    def get_values(self):
        return self.scores

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

    def __init__(self, use_heuristic=True, max_depth = 4):
        super().__init__()

        self.max = None
        self.min = None
        self.max_depth = max_depth
        self.scores = {}
        self.use_heuristic = True
        logger.debug("Depth: " + str(self.max_depth))

    def get_move(self, state):
        self.max = state.get_player_turn()
        self.min = state.get_player_turn(prev=True)

        best_children = []
        best_score = float("-inf")
        for action in state.get_actions():
            _state = deepcopy(state)
            _state.place(action)

            score = self.alphabeta(_state, self.max_depth, float("-inf"), float("inf"), False)
            self.scores[action] = score
            if score > best_score:
                best_children = []
                best_score = score
            if score >= best_score:
                best_children.append(action)
        logger.debug(str(state.get_player_turn()) + " " + str(self.scores))
        return random.choice(best_children)

    def alphabeta(self, state, depth, alpha, beta, max_layer):
        if depth == 1:
            if self.use_heuristic is True:
                return self.heuristic(state, state.get_player_turn(), state.win_span)
            else:
                return 0
        if state.game_over:
            if state.winner == self.max:
                return 100 + depth
            elif state.winner == self.min:
                return -100 - depth
            else:
                return 0

        if max_layer:
            val = float("-inf")
            for action in state.get_actions():
                _state = deepcopy(state)
                _state.place(action)

                val = max(val, self.alphabeta(_state, depth - 1, alpha, beta, False))
                alpha = max(alpha, val)
                if alpha >= beta:
                    break
            return val
        else:
            val = float("inf")
            for action in state.get_actions():
                _state = deepcopy(state)
                _state.place(action)

                old_val = val
                val = min(val, self.alphabeta(_state, depth - 1, alpha, beta, True))
                beta = min(beta, val)
                if alpha >= beta:
                    break
            return val



class Minimax(Algorithm):


    def get_values(self):
        return self.scores

    def __init__(self, use_heuristic = True, max_depth = 4):
        super().__init__()
        self.max = None
        self.min = None
        self.max_depth = max_depth
        self.scores = {}
        self.use_heuristic = use_heuristic
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
        logger.debug(str(state.get_player_turn()) + " " + str(self.scores))
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
            if self.use_heuristic is True:
                return self.heuristic(state, state.get_player_turn(), state.win_span)
            else:
                return 0

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
