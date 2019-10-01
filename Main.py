from Board import *
from Player import *
import time
import pygame
import gym
#import tensorflow as tf

players = [Bot("Green", "MINIMAX", depth=3), Bot("Red")]

completed_games = []


def simulation(players, n = 10, _print=False):
    for i in range(n):
        print("Game: ", i, end = " ")
        board = Board(players)
        while not board.game_over:
            player = board.get_player_turn()
            turn = player.get_choice(board)
            board.place(turn)
            if _print:
                 board.print()
        completed_games.append((board))
        board.print()
        print(board.winner, "(", board.winner.algorithm, ")", " Won!")


def manual(players, sequence):
    board = Board(players)
    bools = board.placeSequence(sequence)

    for i in range(len(board.moves)):
        print("Move: {0}\t{1}".format(board.moves[i], bools[i]))
    completed_games.append(board)


t0 = time.clock()
n = 30
#manual(players, [6, 1, 6, 6, 3, 5, 3, 3, 1, 4, 4, 4, 6, 3, 6, 2, 4, 5])
simulation(players, n, False)
t1 = time.clock()

winners = {}

for board in completed_games:
    board.print()
    print(board.last_move)
    print(board.moves)
    winner = board.check_win()
    if winner in winners:
        winners[winner] += 1
    else:
        winners[winner] = 1
    print(winner)

print("out of {0} games".format(len(completed_games)))
print(winners)
print("Avg time per game: ", (t1 - t0) / n, " seconds per game")

