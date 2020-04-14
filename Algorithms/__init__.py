from Algorithms.Algorithm import *
from Algorithms.MCTS import *
from Algorithms.MCTS_UCT import *
from Algorithms.TDUCT import *
from Algorithms.TDMCTS import *
from Algorithms.Minimax import *
from Core import LOGGER

algorithms = ["MINIMAX", "TDUCT", "UCT", "RANDOM"]
def create_algorithm(args):

    algorithm = args["type"]
    logger.info("Creating " + algorithm)
    if algorithm.upper() == "UCT":
     return MCTS_UCT(n=args.getint("n"), g=args.getfloat("discount_factor"),
                                        e=args.getfloat("exploration"), a = args.getfloat("learning_rate"),memory = args.get("memory", ""))
    elif algorithm.upper() == "TDUCT":
        return MCTS_TDUCT(n=args.getint("n"), g=args.getfloat("discount_factor"),
                                           e=args.getfloat("exploration"), a = args.getfloat("learning_rate"), memory= args.get("memory", ""))

    elif algorithm.upper() == "TDMCTS":
        return MCTS_TDUCT3(n=args.getint("n"), g=args.getfloat("discount_factor"),
                                           e=args.getfloat("exploration"),a = args.getfloat("learning_rate"), memory= args.get("memory", ""))

    elif algorithm.upper() == "test":
        return MCTS_TDUCT3(n=args.getint("n"), g=args.getfloat("discount_factor"),
                                           e=args.getfloat("exploration"),a = args.getfloat("learning_rate"), memory= args.get("memory", ""))

    elif algorithm.upper() == "MINIMAX":
        return Minimax(use_heuristic= args.getboolean("heuristic",False),max_depth= args.getint("depth"))
    elif algorithm.upper() == "ALPHABETA":
        return AlphaBeta_V2(use_heuristic= args.getboolean("heuristic",False), max_depth= args.getint("depth"))
    elif algorithm.upper() == "RANDOM":
        return Random()
    else:
        logger.warning("Defaulting " + str(args["type"] + " to random!"))
        print("Defaulting ", args["type"], " to random.")
        return Random()