from BitBoard import BitBoard
from Player import *
import Algorithm as algo
import math
import numpy as np
import bitstring
from sklearn.preprocessing import OneHotEncoder
from copy import deepcopy
import time
import GameGUI as GUI

players = [ Bot("YELLOW",algorithm=algo.MCTS(n=2000, e=math.sqrt(2))),Bot("red",algorithm=algo.MCTS(n=2000, e=math.sqrt(2)))]

board = BitBoard(players)
board.set_state(players[0], 186132378064173)
board.set_state(players[1], 93126259722898)
GUI.draw([board])
#GUI.play(board, play=False)

