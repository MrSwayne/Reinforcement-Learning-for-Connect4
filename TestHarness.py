from BitBoard import BitBoard
from Player import *
import Algorithm as algo
import NeuralNet as NN
import numpy as np
import bitstring
from sklearn.preprocessing import OneHotEncoder


players = [Bot("blue", algo.MCTS(n=500)), Bot("Red", algo.MCTS(n=500))]

b = BitBoard(players)
#[['0000000000000000000000000000000000000011100000000100000000000000'
 # '0000000000000000000001000000000000010011111000001100000000000000']]
b.place(6)
b.place(0)
b.set_state(players[0], int('0b0000000000000000000000000000000000000011100000000100000000000000',2))
b.set_state(players[1], int('0b0000000000000000000001000000000000010011111000001100000000000000', 2))

print(bin(b.get_state(players[0])[0]))

print(bin(b.get_state(players[1])[0]))

map = {}

import random
for i in range(20):
    for j in range(15):
        map[i,j] = random.randint(0,1)



for state, value in map.items():
    print(state[0], " ", state[1], " ", value)

print(map[19,13])
print(map[(19,13)])

import sys

map[5] = (6,7)

one, two = map[5]

print(one, "->", two)

import Game
Game.draw([b])

