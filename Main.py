#import tensorflow as tf
from Player import *
import time
import Game as Game
import configparser
from GUI import GameGUI as GUI
from Algorithms import *
from BitBoard import *

cfg = configparser.ConfigParser()
cfg.read("config.ini")
players = []

mode = cfg["GENERAL"]["MODE"].upper()

if mode == "TRAIN":
    episodes = cfg["TRAIN"].getint("episodes")
    batch = cfg["TRAIN"].getint("batch")
    tournament_games = cfg["TRAIN"].getint("tournament_games")

    for p in cfg["TRAIN"]["players"].split("\n"):
        players.append(Player.create_player(cfg[p]))

    enemy = Player.create_player(cfg[cfg["TRAIN"]["enemy"]])
    training_res, tournament_res = Game.experiment(players, enemy, episodes, batch, tournament_games)

    print("--\nTraining--\n")
    for completed_games, winners in training_res:
        for game in completed_games:
            print(len(game.moves), end = ", ")
        print()
        print(winners)
        print()

    print("--\nTournament--\n")
    for completed_games, winners in tournament_res:

        for i in range(len(completed_games)):
            game = completed_games[i]
            print(i+1, " ", game.moves)
        for game in completed_games:
            print(len(game.moves), end = ", ")

        print()
        print(winners)
        print()

elif mode == "SIMULATION":
    players = []
    for p in cfg["SIMULATION"]["players"].split("\n"):
        players.append(Player.create_player(cfg[p]))

    completed_games, winners = Game.simulation(players, num_episodes=cfg["SIMULATION"].getint("episodes"), debug=False)

    print(winners)

    if cfg["SIMULATION"].getboolean("train", False):
        for p in players:
            if isinstance(p, Bot):
                p.save("_s")
    GUI.draw(completed_games)

elif mode == "PLAY":
    players = []
    for p in cfg["PLAY"]["players"].split("\n"):
        players.append(Player.create_player(cfg[p]))
    GUI.play(BitBoard(players))

for p in players:
    if isinstance(p, Bot):
        if isinstance(p.algorithm, MCTS):
            p.save()