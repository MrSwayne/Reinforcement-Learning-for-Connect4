#import tensorflow as tf
from Player import *
import time
import Game as Game
from datetime import timedelta
import Algorithm as algo


#players = [Bot("blue", algo.MCTS(duration=timedelta(seconds=2), train=True)), Bot("Red", algo.Minimax(max_depth=4))]
players = [Bot("blue", algo.MCTS(duration=timedelta(seconds=2), learn = True, memory= True, e=0.8)), Bot("Red", algo.MCTS(duration=timedelta(seconds=2), learn = True, memory= True, e=0.8))]
n = 500

t0 = time.clock()
completed_games, new_states = Game.simulation(players, n, _print=False)
t1 = time.clock()

Game.print_results(completed_games)
print("NEW STATES ({0})".format(new_states))
most_moves = 0

print((t1 - t0) / n, "s avg per game")
print(new_states / n, " avg new states" )
Game.draw(completed_games)