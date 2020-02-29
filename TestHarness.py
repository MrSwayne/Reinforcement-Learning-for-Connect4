from GUI import GameGUI as GUI
from Player import *
from Algorithms import *

from BitBoard import *

players = [Human("RED"),Bot("YELLOW", algorithm=AlphaBeta(6))]
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



board = BitBoard(players)


board.place_sequence([0,6,1,6,2,6,3])
print(board.winner)
for p, b in board.boards.items():
    print(b)


print()
for p, b in board.boards.items():
    print(bin(b))