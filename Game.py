import pygame
from BitBoard import *
from Player import *
import time
import pygame
import gym







def simulation(players, n = 10, _print=False):
    completed_games = []
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
        print(board.winner, "(", board.winner.algorithm, ")", " Won!")
    return completed_games


def manual(players, sequence):
    completed_games = []
    board = Board(players)
    bools = board.placeSequence(sequence)

    for i in range(len(board.moves)):
        print("Move: {0}\t{1}".format(board.moves[i], bools[i]))
    completed_games.append(board)
    print(board.get_player_turn())
    return completed_games


def draw(board, width = 1280, height = 720):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    done = False


    player_colour_map = {0:(255,255,255)}

    players = board.get_players()
    for player in players:
        player_colour_map[int(player)] = player.get_rgb()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

        x_offset = 30
        y_offset = 30
        for r in range(board.rows):
            for c in range(board.cols):
                cell = board.get(r, c)
                colour = player_colour_map[cell]

                print(colour)
                pygame.draw.rect(screen, colour, pygame.Rect(x_offset, y_offset, 30, 30))
                x_offset += 31
            x_offset = 30
            y_offset += 31







        pygame.display.flip()


def print_results(completed_games):
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
