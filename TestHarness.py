from Algorithms.MCTS_UCT import MCTS_UCT
from BitBoard import BitBoard
from Player import *
from Algorithms.MCTS_TDUCT import *
from Algorithms.MCTS_TDUCT2 import *
import Algorithm as algo
from Algorithms.Minimax import *
import math
import Game
import numpy as np
import bitstring
from sklearn.preprocessing import OneHotEncoder
from copy import deepcopy
import time
import GameGUI as GUI


def generate_board(players, states):
    board = BitBoard(players)
    for i in range(len(players)):
        board.set_state(players[i], states[i])
    return board


players = [Human("YELLOW"), Bot("RED", algorithm=MCTS_TDUCT2(debug=True))]
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
