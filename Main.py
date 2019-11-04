#import tensorflow as tf
from Player import *
import time
import Game as Game
from datetime import timedelta
import Algorithm as algo


players = [Bot("blue", algo.MCTS(duration=timedelta(seconds=2))), Bot("Red", algo.MCTS(n=50))]

n = 10

t0 = time.clock()
completed_games = Game.simulation(players, n, _print=False)
t1 = time.clock()

Game.print_results(completed_games)
most_moves = 0
longest_game = None
for game in completed_games:

    if len(game.moves) > most_moves:
        most_moves = len(game.moves)
        longest_game = game

print((t1 - t0) / n, " per game")
Game.draw(completed_games)