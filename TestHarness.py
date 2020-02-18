from BitBoard import BitBoard
from Player import *

from GUI import GameGUI as GUI
from Algorithms import *

players = [ Bot("BLUE", algorithm=MCTS_TDUCT(duration=timedelta(seconds=3)), memory="mm"), Human("RED")]

board = BitBoard(players)

board.place_sequence([0,1,2,3,4,5,3,2,5,6,4,3,2,1,2,3])
import time

t0 = time.clock()

for i in range(300):
    _state = deepcopy(board)
    _state.place(random.choice(board.get_actions()))

print( time.clock() - t0)

t0 = time.clock()
for i in range(300):
    b = BitBoard(players)
    for move in board.moves:
        b.place(move)

print(time.clock() - t0)
data = {}

h = Tree.create_tree(board, memory = data)

h.create_children()

h.children[0].visit_count += 1
print(data)


exit(-1)
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