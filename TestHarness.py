from Algorithms.MCTS_UCT import MCTS_UCT
from BitBoard import BitBoard
from Player import *
from Algorithms.MCTS_TDUCT import *
from Algorithms.MCTS_TDUCT2 import *

from Algorithms.Minimax import *
import math
import Game
import numpy as np
import bitstring
from sklearn.preprocessing import OneHotEncoder
from copy import deepcopy
import time
import GameGUI as GUI
from Algorithms.MCTS_TDUCT3 import *

players = [ Bot("BLUE", algorithm=AlphaBeta(4), memory=None),  Bot("RED", algorithm=Minimax(4), memory=None)]

#games, results = Game.simulation(players, 100)
#print(results)
def generate_board(players, states):
    board = BitBoard(players)
    for i in range(len(players)):
        board.set_state(players[i], states[i])
    return board



b = BitBoard(players)

#tree_data = Game.load_tree_data()
#players[0].algorithm.tree_data = tree_data
board = BitBoard(players)

#board.set_state(players[0], 189782802453897)
#board.set_state(players[1], 89475735194166)

#GUI.draw([board])



completed_games = []
'''
for i in range(10):
    board.reset()
    completed_games.append(deepcopy(GUI.play(board, simulation=True)))
 
    '''



GUI.play(board)
#GUI.draw(completed_games)