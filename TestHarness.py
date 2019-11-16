from BitBoard import BitBoard
from Player import *
import Algorithm as algo
players =[Bot("Red", algo.MCTS()), Bot("Green", algo.Random())]
b = BitBoard(players)

b.place(0)
b.place(1)
n = 10000
import time

t1 = time.clock()
for i in range(n):
    bin(b.get_state())
t2 = time.clock()
t3 = time.clock()
for i in range(n):
    b.to_bit_string()

t4 = time.clock()

print(t4-t3, "--", t2-t1)