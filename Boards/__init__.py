from Boards.BitBoard import *
from Boards.ConnectBoard import *
from Boards.TicBoard import *


BOARDS = {"CONNECT4":ConnectBoard,
          "C":ConnectBoard,
          "C4":ConnectBoard,
          "T":TicBoard,
          "TIC":TicBoard,
          "TICTACTOE":TicBoard}

def get_board(txt):
    return BOARDS[txt.upper()]