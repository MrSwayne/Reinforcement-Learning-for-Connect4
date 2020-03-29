from GUI import GameGUI as GUI
from Player import *
from Algorithms import *
from Boards import *

players = [Bot("BLUE", algorithm=MCTS_TDUCT3(n=100, e=1, memory="TTT_Training\max_explore_first_move\\1_4900")),Bot("RED", algorithm=MCTS_TDUCT3(n=100, e=1.616, memory="TTT_Training\max_explore_first_move\\1_4900"))]
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
print(players[0].get_choice(board))
print(players[0].algorithm.root.parent.dump())

completed_games, winners, avg_moves = Game.simulation(TicBoard, players, 50)
#GUI.draw(completed_games)