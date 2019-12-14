#import tensorflow as tf
from Player import *
import time
import Game as Game
from datetime import timedelta
import Algorithm as algo
import NeuralNet as NN

#players = [Bot("blue", algo.MCTS(duration=timedelta(seconds=2), train=True)), Bot("Red", algo.Minimax(max_depth=4))]


neural_net1 = NN.NeuralNet("m1")
neural_net2 = NN.NeuralNet("m2")

players = [Bot("blue", algorithm=algo.MCTS(n=500, e=0.8), neural_net=neural_net1), Bot("Red", algorithm=algo.MCTS(n=500, e=0.8), neural_net=neural_net2) ]
n = 10

t0 = time.clock()


completed_games, new_states = Game.simulation(players, num_episodes=n, _print=False)
t1 = time.clock()


Game.print_results(completed_games)
print("NEW STATES ({0})".format(new_states))
most_moves = 0

print((t1 - t0) / n, "s avg per game")
print(new_states / n, " avg new states" )
Game.draw(completed_games)