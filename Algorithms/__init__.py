from Algorithms.Algorithm import *
from Algorithms.MCTS import *
from Algorithms.MCTS_UCT import *
from Algorithms.MCTS_TDUCT import *
from Algorithms.MCTS_TDUCT2 import *
from Algorithms.MCTS_TDUCT3 import *
from Algorithms.Minimax import *

algorithms = ["MINIMAX", "TDUCT", "UCT", "RANDOM"]

def create_algorithm(args):
    algorithm = args["type"]

    if algorithm.upper() == "UCT":
        return MCTS_UCT(n=args.getint("n"), g=args.getfloat("discount_factor"),
                                        e=args.getfloat("exploration"))
    elif algorithm.upper() == "TDUCT":
        return MCTS_TDUCT3(n=args.getint("n"), g=args.getfloat("discount_factor"),
                                           e=args.getfloat("exploration"))
    elif algorithm.upper() == "MINIMAX":
        return Minimax(args["depth"])
    elif algorithm.upper() == "ALPHABETA":
        return AlphaBeta(args["depth"])
    elif algorithm.upper() == "RANDOM":
        return Random()
    else:
        print("Defaulting ", args["type"], " to random.")
        return Random()