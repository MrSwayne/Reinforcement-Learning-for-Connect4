#import tensorflow as tf
from Player import *
import time
import Game as Game

import GameGUI as GUI
from Algorithms.MCTS import *
from Algorithms.MCTS_UCT import *
from Algorithms.MCTS_TDUCT import *
from Algorithms.MCTS_TDUCT2 import *
import numpy as np
import matplotlib.pyplot as plt
from Algorithms.Minimax import *
from Algorithms.MCTS_TDUCT3 import *
players = [Bot("RED",algorithm=MCTS_TDUCT3(n=200, e=0.05), memory="TD200_e005"),Bot("YELLOW",algorithm=MCTS_TDUCT3(n=200, e=1.414), memory="TD200_e1")]
n = 20



'''
completed_games, winners = Game.simulation(players, num_episodes=n, debug=False)
print(winners)


GUI.draw(completed_games, 3000,3000)
exit(-1)
'''
t0 = time.clock()



#trainee = Bot("Blue", algorithm=MCTS_TDUCT2(n=1000), memory="experiment1")
trainees = [Bot("Blue", algorithm=MCTS_TDUCT3(n=1000), memory="1000_6_E03"), Bot("Orange", algorithm=MCTS_TDUCT3(n=1000), memory="1000_6_E03")]
enemy = Bot("Red", algorithm = AlphaBeta(6))



games, winners = Game.simulation([trainees[0], enemy], num_episodes=100)
print(winners)

training_res, tournament_res = Game.experiment(trainees, enemy, episodes=500, batch=100, tournament_games=100)
for completed_games, winners in tournament_res:
    print(winners)
    GUI.draw(completed_games)

#training_res, tournament_res = Game.experiment(trainees, enemy, episodes=500, batch=100,  tournament_games=100)



states = {}

num_states = []
'''
completed_games, winners = Game.simulation(players, num_episodes=n, table=states, debug=False)
print(winners)
print(num_states)
'''
#t1 = time.clock()

#winner = Game.print_results(completed_games)

#print((t1 - t0) / n, "s avg per game")

#GUI.draw(completed_games)