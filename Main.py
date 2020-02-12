#import tensorflow as tf
from Player import *
import time
import Game as Game
import Algorithm as algo
import GameGUI as GUI
from Algorithms.MCTS import *
from Algorithms.MCTS_UCT import *
from Algorithms.MCTS_TDUCT import *
from Algorithms.MCTS_TDUCT2 import *
import numpy as np
import matplotlib.pyplot as plt
from Algorithms.Minimax import *
#players = [Bot("YELLOW",algorithm=MCTS_TDUCT2(n=1000), memory="positive_reward3"),Bot("RED",algorithm=Minimax(4), memory="positive_reward4")]
n = 10

t0 = time.clock()

#trainee = Bot("Blue", algorithm=MCTS_TDUCT2(n=1000), memory="experiment1")
trainees = [Bot("Blue", algorithm=MCTS_TDUCT2(n=1000), memory="experiment2"), Bot("Blue", algorithm=MCTS_TDUCT2(n=1000), memory="experiment2")]
enemy = Bot("Red", algorithm = Minimax(3))


#Graph avg number of new states -> tesauro way with UCT
#Graph avg number of new states -> TDUCT


results = Game.experiment(trainees, enemy, episodes=500, batch=100, tournament_games=50)
print(results)
#exit(1)


states = {}

num_states = []

completed_games, winners = Game.simulation(players, num_episodes=n, table=states, debug=False)

print(num_states)

#t1 = time.clock()

winner = Game.print_results(completed_games)

#print((t1 - t0) / n, "s avg per game")
for p in players:
    p.save()
GUI.draw(completed_games)