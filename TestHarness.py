#import tensorflow as tf
from Player import *
import time
import Game as Game
from datetime import timedelta
import Algorithm as algo
from Board import Board

players = [Bot("blue", algo.MCTS(duration=timedelta(seconds=2))), Bot("Red", algo.MCTS(n=50))]
board = Board(players)
board.place(5)
print(board.get_state())
print(board.get_last_action())

