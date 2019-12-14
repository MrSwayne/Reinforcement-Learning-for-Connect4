from abc import abstractmethod


class Player():
    num_players = 0

    colours = {
        "RED":((255,0,0)),
        "GREEN":(0,255,0),
        "BLUE":(0,0,255),
        "BLACK":(0,0,0),
        "WHITE":(255,255,255)
    }

    def __init__(self, colour):
        Player.num_players += 1

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


class Human(Player):

    def __init__(self, colour):
        Player.__init__(self, colour)

    def get_choice(self, board):
        actions = board.get_actions()
        board.print()
        print("Select from: ", actions , end=": ")
        user_action = input()

        return int(user_action)

class Bot(Player):

    def __init__(self, colour, algorithm, neural_net = None):
        Player.__init__(self, colour)
        self.best_choice = -1
        self.algorithm = algorithm
        self.neural_net = neural_net

    def get_choice(self, board):
        return self.algorithm.get_move(state=board, player = self)
