import bitstring as bs
import random
import BitBoard as bt
from Player import *
rows = 6
cols = 7


def print_bits(bitString):
    for r in range(rows):
        row = (r + 1) * cols
        print(bitString[row: row + cols].bin)


string = ""
for r in range(rows+1):
    for c in range(cols):
        if r == 0:
            string += "0"
        else:
            string += str(random.choice([0,1]))




board = bs.BitArray(bin="0000000" + "0000001" + "0000001" + "0000001" + "0000001" + "0000000" + "0000000")
#board = bs.BitArray(bin=string)



players = [Bot("Green", "MCTS", depth=3), Bot("Red", "RANDOM", depth= 3)]
board = bt.Board(players)





