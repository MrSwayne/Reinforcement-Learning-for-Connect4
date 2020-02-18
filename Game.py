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

def experiment(trainee, enemy, episodes = 500, batch= 100, tournament_games = 100):

    memory = "experiments/" + datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    trainees = [Bot("BLUE", algorithm=trainee, memory=memory), Bot("ORANGE", algorithm=trainee, memory=memory)]

    enemy = Bot("RED", algorithm=enemy)

    tournament_number = 1

    training_results = []
    tournament_results = []
    i = 0
    while i < episodes:

        #Train

        best_winner = None
        if i != 0:
            print("Training ", i, "-", i + batch)

            t0 = time.clock()
            completed_games, winners = simulation(trainees, num_episodes=batch)
            t1 = time.clock()
            print("Training ", batch, " games = ", t1-t0, " seconds")
            training_results.append(winners)
            c = float("-inf")
            for winner, count in winners.items():
                if count >= c:
                    best_winner = winner
                    c = count
            i += batch

        if best_winner == None:
            best_winner = trainees[0]

        if random.randint(0,10) < 5:
            players = [best_winner, enemy]
        else:
            players = [enemy, best_winner]

        #Tournament
        print("Tournament ", tournament_number, "\t", players)

        t0 = time.clock()

        completed_games, winners = simulation(players, tournament_games)

        t1 = time.clock()
        print("Tournament ", tournament_games, " games = ", t1 - t0, " seconds")

        print(winners)
        tournament_number += 1

        tournament_results.append(winners)
    return training_results, tournament_results

def simulation(players, num_episodes=10, table = {}, debug=False):
    completed_games = []

    state = create_board(players)
    winners = {}

    try:
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
                winner = state.check_win()

            if winner in winners:
                winners[winner] += 1
            else:
                winners[winner] = 1

            print(winner, " ", len(state.moves))
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
