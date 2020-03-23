from GUI import GameGUI as GUI
from Player import *
from Algorithms import *
from Boards import *

players = [Bot("RED", algorithm=MCTS_TDUCT3(n=1000,memory="train/ttt/1_100")),Bot("RED", algorithm=MCTS_TDUCT3(n=1000, memory="train/ttt/1_150"))]
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
board = TicBoard(players)

players[0].get_choice(board)
print(players[0].algorithm.root.parent.dump())

players[1].get_choice(board)
print(players[1].algorithm.root.parent.dump())

n = 0

GUI.draw(board)