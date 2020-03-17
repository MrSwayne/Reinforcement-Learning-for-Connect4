from GUI import GameGUI as GUI
from Player import *
from Algorithms import *

from BitBoard import *

players = [Bot("YELLOW", algorithm=MCTS_TDUCT3(n=1500, memory="")), Human("RED")]
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

#board.set_state(players[0], 176208906699180)
#board.set_state(players[1], 101400464162835)
GUI.play(board)