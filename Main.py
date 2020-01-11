#import tensorflow as tf
from Player import *
import time
import Game as Game
import GameGUI as GUI
from datetime import timedelta
import Algorithm as algo
import math
import GameGUI as GUI
#import NeuralNet as NN

#players = [Bot("blue", algo.MCTS(duration=timedelta(seconds=2), train=True)), Bot("Red", algo.Minimax(max_depth=4))]



#neural_net1 = NN.NeuralNet("m1")
#neural_net2 = NN.NeuralNet("m2")


players = [Bot("YELLOW",algorithm=algo.MCTS(duration=timedelta(seconds=2), e=1.414, memory=True)), Bot("RED", algorithm=algo.MCTS(duration=timedelta(seconds=2), e=1.414, memory=True))]
n = 10
t0 = time.clock()


completed_games, new_states = Game.simulation(players, num_episodes=n, _print=False)
t1 = time.clock()

winner = Game.print_results(completed_games)

print("NEW STATES ({0})".format(new_states))
most_moves = 0

print((t1 - t0) / n, "s avg per game")
print(new_states / n, " avg new states" )
GUI.draw(completed_games)