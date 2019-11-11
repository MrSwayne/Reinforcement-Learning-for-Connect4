from BitBoard import BitBoard
from Player import *
import Algorithm as algo
players =[Bot("Red", algo.MCTS()), Bot("Green", algo.Random())]
b = BitBoard(players)
