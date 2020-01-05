from BitBoard import BitBoard
from Player import *
import Algorithm as algo
import math
import numpy as np
import bitstring
from sklearn.preprocessing import OneHotEncoder
import GameGUI as GUI

players = [ Human("Green"), Human("Red")]#Bot("red",algorithm=algo.MCTS(n=700, e=math.sqrt(2)))]

board = BitBoard(players)

GUI.play(board)



