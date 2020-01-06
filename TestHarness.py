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

players = [ Human("Green"), Human("Red")]#Bot("red",algorithm=algo.MCTS(n=700, e=math.sqrt(2)))]

board = BitBoard(players)
board.set_state(players[0], 180904303591687)
board.set_state(players[1], 97238598598808)
board.print()
GUI.play(board)

