import pygame
from Board import *
from Player import *
import Algorithm as algo
import time


def simulation(players, n = 10, _print=False):
    completed_games = []
    for i in range(n):
        print("Game: ", i)
        board = Board(players)
        prev_turn = -1
        while not board.game_over:
            player = board.get_player_turn()
            turn = player.get_choice(board)

            board.place(turn)

            winner = board.check_win()
            if _print:
                 board.print()
        completed_games.append((board))
        if isinstance(winner.algorithm, algo.MCTS):
            winner.algorithm.save_data()
        if isinstance(winner, Bot):
            print(winner, "(", winner.algorithm, ")", " Won!")
        else:
            print(winner, " (Human) Won!")
    return completed_games


def manual(players, sequence):
    print("WTF")
    completed_games = []
    board = Board(players)
    bools = board.placeSequence(sequence)
    board.print()
    for i in range(len(board.moves)):
        print("Move: {0}\t{1}".format(board.moves[i], bools[i]))
    completed_games.append(board)
    print(board.get_player_turn())
    return completed_games


def draw(boards, width = 1280, height = 720):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    done = False


    player_colour_map = {0:(255,255,255)}

    players = boards[0].get_players()
    for player in players:
        player_colour_map[player] = player.get_rgb()


    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                break
                print(pygame.mouse.get_pos())

        board_offset_x = 0
        board_offset_y = 0

        count = 1
        for board in boards:


            x_offset = 30 + board_offset_x
            y_offset = 30 + board_offset_y

            for r in range(board.rows):
                for c in range(board.cols):
#            for r in range(board.rows - 1, -1, -1):
#                for c in range(0, board.cols):
                    cell = board.get(r, c)

                    try:
                        colour = player_colour_map[cell]
                    except:
                        colour = player_colour_map[0]

                    pygame.draw.rect(screen, colour, pygame.Rect(x_offset, y_offset, 30, 30))
                    x_offset += 31
                x_offset = 30 + board_offset_x
                y_offset += 31
            board_offset_y = y_offset + 2

            if count % 3 == 0:
                board_offset_x += 260
                board_offset_y = 0

            count += 1

        pygame.display.flip()


def print_results(completed_games):
    winners = {}
    for board in completed_games:
        board.print()

        winner = board.check_win()
        if winner in winners:
            winners[winner] += 1
        else:
            winners[winner] = 1
        print(winner)

    print("out of {0} games".format(len(completed_games)))
    print(winners)
