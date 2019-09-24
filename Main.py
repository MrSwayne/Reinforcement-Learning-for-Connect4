from Board import *
from Player import *
import gym
#import tensorflow as tf

p = Bot("Green", "RANDOM")
b = Bot("Red", "MINIMAX")

players = [p, b]


completed_games = []


def simulation(players, n = 10, _print=False):
    for i in range(n):
        print(i)
        board = Board(players)
        while not board.game_over:
            player = board.get_player_turn()
            turn = player.get_choice(board)
            board.place(turn)
            if _print:
                 board.print()
        completed_games.append((board))


def manual(players, sequence):
    board = Board(players)
    bools = board.placeSequence(sequence)

    for i in range(len(board.moves)):
        print("Move: {0}\t{1}".format(board.moves[i], bools[i]))
    completed_games.append(board)

#seq = [0,1,0,1,0,1,0,1,0]
#seq= [6, 6, 1, 6, 5, 6, 4, 5, 6,6,4,3]# 4, 5, 5, 5, 1, 5, 0, 4, 1, 4, 2, 4, 3]
#manual(players, seq)


simulation(players, 10, True)



count = 0
for board in completed_games:
    board.print()
    print(board.moves)
    winner = board.check_win()
    print(winner)
    if winner == b:
        count += 1

print(b, " won ", count, end= " ")
print("out of {0} games".format(len(completed_games)))

