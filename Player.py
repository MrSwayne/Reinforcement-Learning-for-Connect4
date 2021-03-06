from abc import abstractmethod
import Algorithms
from Core import LOGGER

logger = LOGGER.attach(__name__)

class Player():

    @staticmethod
    def create_player(args):
        if (args["type"].upper() == "HUMAN"):
            logger.info("Creating Human " + args["colour"])
            return Human(args["colour"])
        else:
            logger.info("Creating Bot " + args["colour"])
            algorithm = Algorithms.create_algorithm(args)

            return Bot(args["colour"], algorithm)

    num_players = 0

    colours = {
        "RED":((255,0,0)),
        "GREEN":(0,255,0),
        "BLUE":(0,0,255),
        "BLACK":(0,0,0),
        "WHITE":(255,255,255),
        "YELLOW":(255,255,0),
        "AQUA":(0,128,128),
        "GRAY":(128,128,128),
        "NAVY":(0,0,128),
        "ORANGE":(265,165,0)
    }

    def set_learning(self, bool):

        logger.info("Setting learning to " + str(bool) + " for " + self.colour)
        self.algorithm.set_learning(bool)

    def __init__(self, colour):
        Player.num_players += 1
        self.algorithm = None
        if colour.upper() in self.colours:
            self.colour = colour.upper()
        else:
            self.colour = "BLACK"
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

    def get_rgb(self):
        return self.colours[self.colour]

    @abstractmethod
    def save(self):
        pass

import random
class Human(Player):

    def __init__(self, colour):
        Player.__init__(self, colour)

    def get_choice(self, board):
        actions = board.get_actions()
        board.print()
        print("Select from: ", actions , end=": ")
        user_action = int(input())
        return user_action

class Bot(Player):

    def __init__(self, colour, algorithm):
        Player.__init__(self, colour)
        self.best_choice = -1
        self.algorithm = algorithm
        self.learning = True

    def get_choice(self, board):

        return self.algorithm.get_move(state=board)

    def clear_memory(self):
        print(self.colour, ": clearing memory")
        self.algorithm.clear_memory()

    def save(self, tag = ""):
        self.algorithm.save_memory(tag)