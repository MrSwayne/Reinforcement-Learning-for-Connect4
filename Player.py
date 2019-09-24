from abc import ABC, abstractmethod
import random
from Board import *

class Player():
    num_players = 0
    def __init__(self, colour):
        Player.num_players += 1
        self.colour = colour
        self.number = Player.num_players

    @abstractmethod
    def get_choice(self, board):
        pass

    def __repr__(self):
        return self.colour

    def __str__(self):
        return self.colour

    def __int__(self):
        return self.number

class Human(Player):

    def __init__(self, colour):
        Player.__init__(self, colour)

    def get_choice(self, board):
        return random.choice(board.get_actions())

class Bot(Player):

    algorithms = ["MINIMAX", "MCTS", "RANDOM"]
    def __init__(self, colour, algorithm = "RANDOM"):
        Player.__init__(self, colour)
        self.best_choice = -1

        if algorithm.upper() in Bot.algorithms:
            self.algorithm = algorithm.upper()
        else:
            print("Algorithm ", algorithm, " not found. Defaulting to RANDOM")
            self.algorithm = "RANDOM"


    def minimaxHeuristic(self, board):
        state = board.get_state();

        self_score = 0
        opp_score = 0

        opp_in_a_row = 0
        for r in range(board.rows):
            for c in range(board.cols):
                if state[r,c] == 0:
                    continue
                if state[r, c] == int(self):
                    neighbours = board.get_neighbours(r, c)

                    temp_score = 0
                    for neighbourTuple in neighbours:
                        temp_score += neighbourTuple[0]
                        temp_score += neighbourTuple[1]
                    self_score += temp_score
                else:
                    neighbours = board.get_neighbours(r, c)
                    temp_score = 0
                    for neighbourTuple in neighbours:
                        temp_score += neighbourTuple[0]
                        temp_score += neighbourTuple[1]
                    opp_score += temp_score

        return (self_score - opp_score) if board.get_player_turn() == self else -(self_score - opp_score)




    def minimax(self, board, maxLayer = True, current_depth = 0, max_depth = 4):

        winner = board.check_win(step=True)
        if winner == self:
            return 10000 - current_depth * 10
        elif winner in board.players:
            return -1000000
        elif int(winner) == 0:
            return 0

        if current_depth == max_depth:
            return self.minimaxHeuristic(board)

        max_score = 0


        actions = board.get_actions()
        for action in actions:
            score = 0
            new_board = board.clone()

            new_board.place(action)
            score += self.minimax(new_board, not maxLayer, current_depth + 1) + self.minimaxHeuristic(board)
            if score >= max_score:
                max_score = score
                self.best_choice = action
        return max_score

    def get_choice(self, board):
        if self.algorithm == "RANDOM":
            return random.choice(board.get_actions())
        elif self.algorithm == "MINIMAX":
            self.minimax(board)
            return self.best_choice
        else:
            return None
