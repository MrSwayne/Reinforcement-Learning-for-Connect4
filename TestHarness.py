from BitBoard import BitBoard
from Player import *
import Algorithm as algo
import bitstring
players =[Bot("Red", algo.MCTS()), Bot("Green", algo.Random())]
b = BitBoard(players)

b.place_sequence([0,3,2,3,2,3,2,2,1,3])

for r in range(b.rows):
    for c in range(b.cols):
        print(b.get_index(r, c), end = " ")
    print()

import time

for p, b in b.boards.items():
    t0 = time.clock()
    for i in range(10000):
        bin(b)

    t1 = time.clock()
    print(t1 - t0)
n = 10000
import time


