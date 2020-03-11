from Algorithms.Algorithm import *
from Algorithms.MCTS import *
from Algorithms.MCTS_UCT import *
from Algorithms.MCTS_TDUCT import *
from Algorithms.TDUCT_2 import *
from Algorithms.TDUCT_3 import *
from Algorithms.Minimax import *

algorithms = ["MINIMAX", "TDUCT", "UCT", "RANDOM"]

def create_algorithm(args):
    algorithm = args["type"]

    if algorithm.upper() == "UCT":
        return MCTS_UCT(n=args.getint("n"), g=args.getfloat("discount_factor"),
                                        e=args.getfloat("exploration"), memory = args.get("memory", ""))
    elif algorithm.upper() == "TDUCT":
        return MCTS_TDUCT(n=args.getint("n"), g=args.getfloat("discount_factor"),
                                           e=args.getfloat("exploration"), memory= args.get("memory", ""))

    elif algorithm.upper() == "TDUCT2":
        return MCTS_TDUCT2(n=args.getint("n"), g=args.getfloat("discount_factor"),
                                           e=args.getfloat("exploration"), memory= args.get("memory", ""))
    elif algorithm.upper() == "TDUCT3":
        return MCTS_TDUCT3(n=args.getint("n"), g=args.getfloat("discount_factor"),
                                           e=args.getfloat("exploration"), memory= args.get("memory", ""))
    elif algorithm.upper() == "MINIMAX":
        return Minimax(args.getint("depth"))
    elif algorithm.upper() == "ALPHABETA":
        return AlphaBeta(args.getint("depth"))
    elif algorithm.upper() == "ALPHABETA_H":
        return AlphaBeta_h(args.getint("depth"))
    elif algorithm.upper() == "RANDOM":
        return Random()

    else:
        print("Defaulting ", args["type"], " to random.")
        return Random()