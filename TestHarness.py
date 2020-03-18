from GUI import GameGUI as GUI
from Player import *
from Algorithms import *

from BitBoard import *




players = [Bot("YELLOW", algorithm=MCTS_UCT(n=1000, e = 0.25)), Human("RED")]
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
from Game import *
'''
board.place_sequence([3, 3, 3, 3, 2, 1, 2, 2, 2, 4, 4, 5, 5, 5, 0, 3, 0, 2,
2, 1, 0, 0, 3, 4, 0, 4, 4, 4, 5, 0, 5, 5])
print(players[0].get_choice(board))

players[0].algorithm.root.print()

board.place(1)
print(board.boards)
print(board.winner)
print(players[1].get_choice(board))
players[1].algorithm.root.print()
board.place_sequence([1])
print(board.boards)
print(board.winner)
#board.set_state(players[0], 176208906699180)
#board.set_state(players[1], 101400464162835)
GUI.draw([board])
'''
GUI.play(board)