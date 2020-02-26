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




moves = [3, 2, 2, 3, 3, 2, 3, 5, 5, 3, 2, 6, 2, 6, 4, 1, 6, 6, 1, 2, 1, 5, 5, 5, 4, 4, 4]


board = BitBoard(players)

GUI.play(board)
# #board.place_sequence([3, 2, 2, 3, 3, 2, 3, 5, 5, 3, 2, 6, 2, 6, 4, 1, 6, 6, 1, 6, 1, 5, 5, 5, 4, 4])
print(board.boards)
GUI.draw([board])
'''
z = []
z.append([3,4,1,1,0,0,2])
z.append([3, 2, 5, 2, 6, 4, 4, 4, 6, 5, 2, 4, 6, 6, 2, 4, 4, 1, 1, 2, 1, 5, 1, 1, 5, 6, 1, 2, 6, 3, 3])
z.append([3, 2, 5, 2, 6, 4, 4, 4, 6, 5, 2, 4, 6, 6, 2, 4, 4, 2, 0, 1, 0, 0, 0, 2, 0, 5, 5, 6, 1, 3, 3])
z.append([3, 2, 5, 2, 6, 4, 4, 4, 6, 5, 2, 4, 6, 6, 2, 1, 2, 2, 4, 5, 5, 1, 1, 0, 0, 1, 5, 1, 0, 0, 5, 3, 3])
z.append([3, 2, 5, 2, 6, 4, 4, 4, 6, 5, 2, 4, 2, 1, 2, 2, 4, 5, 5, 1, 1, 6, 1, 1, 6, 0, 0, 5, 1, 0, 6, 3, 3])
boards = []
for moves in z:
    b = BitBoard(players)
    for move in moves:
        b.place(move)
    boards.append(b)
'''
#GUI.draw(boards)