from GUI import GameGUI as GUI
from Player import *
from Algorithms import *
from Boards import *

players = [Bot("BLUE", algorithm=MCTS_UCT(n=1000, e=0.5, memory="")),Bot("RED", algorithm=MCTS_TDUCT3(n=1000, e=0.5, memory=""))]
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


#ame.simulation(TicBoard, players, 10)
board = ConnectBoard(players)
GUI.play(board)