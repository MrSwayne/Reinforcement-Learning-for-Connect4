#import tensorflow as tf
from Player import *
import time
import Game as Game
from Board import *

players = [Bot("Green", "MCTS",simulations=10, depth=4), Bot("Red", "MINIMAX", simulations=10,depth= 4)]


n = 5


t0 = time.clock()
completed_games = Game.simulation(players, n, False)
t1 = time.clock()

Game.print_results(completed_games)
print(completed_games[0].board)
print(completed_games[0].get_actions())

#games = Game.manual(players, [2,2,2,3,6,5,2,2, 2])

print((t1 - t0) / n, " per game")