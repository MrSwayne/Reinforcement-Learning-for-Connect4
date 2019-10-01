from abc import ABC, abstractmethod
import random
from Board import *
from copy import deepcopy

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
        actions = board.get_actions()
        print("Select from: ", actions , end=": ")
        user_action = input()

        return random.choice(board.get_actions())

class Bot(Player):


    algorithms = ["MINIMAX", "MCTS", "RANDOM"]
    def __init__(self, colour, algorithm = "RANDOM", depth=3):
        Player.__init__(self, colour)
        self.best_choice = -1
        self.depth = depth
        if algorithm.upper() in Bot.algorithms:
            self.algorithm = algorithm.upper()
        else:
            print("Algorithm ", algorithm, " not found. Defaulting to RANDOM")
            self.algorithm = "RANDOM"



    def minimaxHeuristic(self, board):
        state = board.get_state();

        heuristic_score = 0

        modifier = 1
        for r in range(board.rows):
            for c in range(board.cols):
                if state[r,c] == 0:
                    continue

                cell_to_check = state[r, c]

                if cell_to_check == int(self):
                    modifier = 1
                else:
                    modifier = -1

                neighbours = board.get_neighbours(r, c)
                directions = list(neighbours.keys())

                for i in range(0 ,len(directions) - 1, 2):
                    number_of_neighbours = 0
                    positive_direction = neighbours[directions[i]]
                    negative_direction = neighbours[directions[i + 1]]

                    opposite_directions = [positive_direction, negative_direction]

                    number_of_blanks = 0
                    score = 0
                    for direction in opposite_directions:

                        for neighbour in direction:
                            if neighbour == cell_to_check:
                                number_of_neighbours += 1
                            #elif neighbour == 0:
                               # number_of_blanks += 1

                    if (number_of_neighbours) >= (board.win_span - 1):
                        return 10000000 * modifier


                    score += (10 ** (number_of_neighbours ))#* number_of_blanks))
                    heuristic_score += score * modifier

        return heuristic_score




    def minimax(self, board, current_depth = 0):

        winner = board.check_win(step=True)
        if winner == self:
            return 100000000000 - current_depth * 10
        elif winner in board.players:
            return -10000000
        elif int(winner) == 0:
            return 0

        if current_depth == self.depth:
            return self.minimaxHeuristic(board)

        max_score = 0

        actions = board.get_actions()

        choices = []
        for action in actions:
            score = 0
            new_board = deepcopy(board)

            new_board.place(action)
            score += self.minimax(new_board, current_depth + 1)

            if score == max_score:
                choices.append(action)

            elif score > max_score:
                max_score = score
                choices.clear()
                choices.append(action)

        if len(choices) > 0 and current_depth == 0:
            self.best_choice = random.choice(choices)
        return max_score

    def mcts(self,  board):
        pass

    def get_choice(self, board):
        if self.algorithm == "RANDOM":
            return random.choice(board.get_actions())
        elif self.algorithm == "MINIMAX":
            self.minimax(board)
            return self.best_choice
        elif self.algorithm == "MCTS":
            self.mcts(board)
            return self.best_choice
        else:
            return None
