import pygame
from copy import deepcopy
from BitBoard import *
import time
from Player import *
from Algorithms.MCTS_UCT import *
from Algorithms.MCTS import *
#from keras.utils import to_categorical
import time
import os
import csv
import pandas
from datetime import datetime

def create_board(players):
    return BitBoard(players)

def experiment(players, enemy, episodes = 500, batch= 100, tournament_games = 100):

    tournament_number = 1
    training_results = []
    tournament_results = []
    i = 0
    data = None
    for p in players:
        if data is None:
            data = p.algorithm.get_memory()
        else:
            p.algorithm.set_memory(data)

    while i < episodes:
        #Train
        if i != 0:
            for p in players:
                p.set_learning(True)

            print("Training ", i, "-", i + batch - 1)

            t0 = time.clock()
            completed_games, winners, avg_moves = simulation(players, num_episodes=batch)
            t1 = time.clock()
            print("Training ", batch, " games = ", t1-t0, " seconds")
            training_results.append((completed_games, winners, avg_moves))
            c = float("-inf")
            i += batch
            players[0].save("_" + str(i - 1))
        else:
            i += 1

        tournament_players = [players[0], enemy]
        #Tournament
        print("Tournament ", tournament_number, "\t", tournament_players)

        for p in tournament_players:
            p.set_learning(False)

        t0 = time.clock()
        completed_games, winners, avg_moves = simulation(tournament_players, tournament_games)

        t1 = time.clock()
        print("Tournament ", tournament_games, " games = ", t1 - t0, " seconds")
        print(winners)
        tournament_number += 1
        tournament_results.append((completed_games, winners, avg_moves))

    return training_results, tournament_results

def simulation(players, num_episodes=10, table = {}, debug=False):
    completed_games = []

    state = create_board(players)
    winners = {}
    prev_total_states = 0

    avg = 0
    for i in range(num_episodes):
        print("Game ", (i+1), end = " - " )
        state.reset()
        winner = None
        while not state.game_over:

            if state.get_state() not in table:
                table[state.get_state()] = 1
            else:
                table[state.get_state()] += 1

            if debug:
                state.print()

            player = state.get_player_turn()

            action = player.get_choice(state)
            state.place(action)
            winner = state.winner
        avg += len(state.moves)
        if winner in winners:
            winners[winner] += 1
        else:
            winners[winner] = 1

        print(winner, " ", len(state.moves))

        completed_games.append(deepcopy(state))

    return completed_games, winners, avg / num_episodes

def manual(players, sequence):
    completed_games = []
    state = create_board(players)
    bools = []
    for move in sequence:
        bools.append(state.place(move))

    state.print()
    for i in range(len(state.moves)):
        print("Move: {0}\t{1}".format(state.moves[i], bools[i]))
    completed_games.append(state)
    print(state.get_player_turn())
    return completed_games

def print_results(completed_games):
    winners = {}
    for i in range(len(completed_games)):
        state = completed_games[i]
       # state.print()

        print(i+1, end="\t")
        for p in state.players:
            print(state.get_state(p), end = ";")
        print()
        print(state.moves)

        winner = state.check_win()
        if winner in winners:
            winners[winner] += 1
        else:
            winners[winner] = 1
        print(winner)

    print("out of {0} games".format(len(completed_games)))

    max_score = 0
    most_wins = None
    for winner, score in winners.items():
        if score > max_score:
            max_score = max_score
            most_wins = winner
    print(winners)
    return most_wins
