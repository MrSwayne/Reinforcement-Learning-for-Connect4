import pygame
from copy import deepcopy
from BitBoard import *

from Player import *
from Algorithms.MCTS_UCT import *
from Algorithms.MCTS import *
#from keras.utils import to_categorical
import time
import os
import csv
import pandas


def create_board(players):
    return BitBoard(players)

def experiment(trainees, enemy, episodes, batch, tournament_games = 10):

    tournament_number = 1

    res = []
    for i in range(episodes):

        #Train

        print("Training ", (i+1), "-", i + batch)
        completed_games, winners = simulation(trainees, num_episodes=batch)

        best_winner = None
        c = float("-inf")
        for winner, count in winners.items():
            if count >= c:
                best_winner = winner
                c = count

        i += batch

        tag = "_" + str(i + 1)
        if i == episodes - 1:
            tag = ""

        if isinstance(best_winner, Bot):
            best_winner.save(tag)
            for p in trainees:
                if p is not best_winner and isinstance(p, Bot):
                    p.algorithm.tree_data = best_winner.algorithm.tree_data

        players = [best_winner, enemy]
        #Tournament
        print("Tournament ", tournament_number)
        completed_games, results = simulation(players, tournament_games)

        print(results)
        tournament_number += 1

        res.append(results)
    return res

def simulation(players, num_episodes=10, table = {}, debug=False):
    completed_games = []

    state = create_board(players)
    winners = {}
    try:
        for i in range(num_episodes):
            print("Game ", (i+1))
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
                winner = state.check_win()

            if winner in winners:
                winners[winner] += 1
            else:
                winners[winner] = 1

            completed_games.append(deepcopy(state))

    except KeyboardInterrupt:
        for p in players:
            p.save()
        return completed_games, winners

    return completed_games, winners

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
