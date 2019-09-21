from Board import *
from Player import *
import gym
#import tensorflow as tf

p = Human("Green")
b = Bot("Red", "MINIMAX")



games = []
for i in range(1000):
    print(i)
    board = Board([p, b])
    while not board.game_over:
        player = board.get_player_turn()
        turn = player.get_choice(board)
        print(turn)
        board.place(turn)
        winner = board.check_win()
        board.print()
    games.append((winner, board.get_state(), board.moves))

map = dict()

for game in games:
    if game[0] in map:
        map[game[0]] += 1
    else:
        map[game[0]] = 0

print(map)
