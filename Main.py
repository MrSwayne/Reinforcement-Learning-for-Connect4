import os
#import tensorflow as tf
from Player import *
import time
import Game as Game
import configparser
from GUI import GameGUI as GUI
from Algorithms import *
from BitBoard import *
random.seed(10)
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
    for completed_games, winners, avg_moves in training_res:

        print(winners, "\t", avg_moves)
        print()

    print("--\nTournament--\n")
    for completed_games, winners, avg_moves in tournament_res:
        avg = 0

        print(winners, "\t", avg_moves)
        print()

elif mode == "SIMULATION":
    players = []
    for p in cfg["SIMULATION"]["players"].split("\n"):
        player = Player.create_player(cfg[p])
        players.append(player)
        player.set_learning(False)


    path =cfg["SIMULATION"].get("path", "")
    if path is not "":
        head, file = os.path.split(path)
    completed_games, winners, avg_states = Game.simulation(players, num_episodes=cfg["SIMULATION"].getint("episodes"), debug=False)

    print()
    print(winners, "\t", avg_states)

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