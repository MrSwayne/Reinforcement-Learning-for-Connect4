<<<<<<< HEAD
from Core import LOGGER
LOGGER.filename = "testHarness"
from GUI import GameGUI as GUI
from Player import *
from Algorithms import *
from Boards import *
from matplotlib import colors as COLOURS


import multiprocessing as mp


players = [Bot("RED", algorithm=MCTS_UCT(n=500,e = 0.5, memory="hello/2_max_5000")), Human("BLUE")]
def get_states(data, moves):
    states = {}
    boards = []
    b = BitBoard(players)
    for move in moves:
        b.place(move)
        _b = deepcopy(b)
        boards.append(_b)
        states[b.get_state()] = _b

    for state, node in data.items():
        if state in states:
            print(boards.index(states[state]), ". ", state, " ", node)


import Game

import sys
print(sys.maxsize)
#ame.simulation(TicBoard, players, 10)
board = ConnectBoard(players)
GUI.play(board)
=======
from Core import LOGGER
LOGGER.filename = "testHarness"
from GUI import GameGUI as GUI
from Player import *
from Algorithms import *
from Boards import *
from matplotlib import colors as COLOURS


import multiprocessing as mp


players = [Human("YELLOW"), Human("BLUE")]
def get_states(data, moves):
    states = {}
    boards = []
    b = BitBoard(players)
    for move in moves:
        b.place(move)
        _b = deepcopy(b)
        boards.append(_b)
        states[b.get_state()] = _b

    for state, node in data.items():
        if state in states:
            print(boards.index(states[state]), ". ", state, " ", node)


import Game

import sys
print(sys.maxsize)
#ame.simulation(TicBoard, players, 10)
board = ConnectBoard(players)
GUI.play(board)
>>>>>>> 391e228... graph time
