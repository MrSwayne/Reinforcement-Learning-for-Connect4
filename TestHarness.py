
from Core import LOGGER
LOGGER.filename = "testHarness"
from GUI import GameGUI as GUI
from Player import *
from Algorithms import *
from Boards import *
from matplotlib import colors as COLOURS


import multiprocessing as mp


players = [Human("BLUE"),Human("RED") ]

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

for i in range(10000):

    if i % 200 == 0:
        print(i)

import Game

import sys
print(sys.maxsize)
#ame.simulation(TicBoard, players, 10)
board = TicBoard(players)
GUI.play(board)

