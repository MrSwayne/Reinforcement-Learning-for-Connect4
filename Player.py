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

        if algorithm.upper() in Bot.algorithms:
            self.algorithm = algorithm.upper()
        else:
            print("Algorithm ", algorithm, " not found. Defaulting to RANDOM")
            self.algorithm = "RANDOM"


    def minimax(self, board, maxLayer = True, current_depth = 0, max_depth = 2):
        newBoard = board.clone()

        if current_depth == max_depth:
            return 5

        winner = newBoard.check_win()
        if winner == self:
            return 100 - current_depth
        elif winner in newBoard.players:
            return -100 + current_depth
        elif int(winner) == 0:
            return 0

        score = 0
        max_score = 0
        best_choice = -1

        while not newBoard.game_over:
            actions = newBoard.get_actions()
            for action in actions:
                newBoard.place(action)
                score = self.minimax(newBoard, not maxLayer, current_depth + 1)

                if score > max_score:
                    max_score = score
                    best_choice = action
        if best_choice < 0 and not newBoard.game_over:
            return random.choice(newBoard.get_actions())
        return best_choice

    def get_choice(self, board):
        if self.algorithm == "RANDOM":
            return random.choice(board.get_actions())
        elif self.algorithm == "MINIMAX":
            return self.minimax(board)
        else:
            return None
