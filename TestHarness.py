from BitBoard import BitBoard
from Player import *

from GUI import GameGUI as GUI
from Algorithms.MCTS_TDUCT3 import *

players = [ Bot("BLUE", algorithm=MCTS_TDUCT3(duration=timedelta(seconds=3)), memory="mm"), Human("RED")]

#print(results)
def generate_board(players, states):
    board = BitBoard(players)
    for i in range(len(players)):
        board.set_state(players[i], states[i])
    return board

board = BitBoard(players)

GUI.play(board, W=2000, H=2160)

completed_games = []
'''
for i in range(10):
    board.reset()
    completed_games.append(deepcopy(GUI.play(board, simulation=True)))
 
    '''

GUI.play(board)
players[1].save()
#GUI.draw(completed_games)