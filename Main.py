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

if cfg["GENERAL"]["MODE"] == "TRAIN":
    episodes = cfg["TRAIN"].getint("episodes")
    batch = cfg["TRAIN"].getint("batch")
    tournament_games = cfg["TRAIN"].getint("tournament_games")
    trainee = cfg["TRAIN"]["trainee"]
    trainee = create_algorithm(cfg[trainee])
    enemy = cfg["TRAIN"]["enemy"]
    enemy = create_algorithm(cfg[enemy])

    training_res, tournament_res = Game.experiment(trainee, enemy, episodes, batch, tournament_games)

    print(tournament_res)
elif cfg["GENERAL"]["MODE"] == "SIMULATION":
    players = []
    for p in cfg["SIMULATION"]["players"].split("\n"):
        players.append(Player.create_player(cfg[p]))
    completed_games, winners = Game.simulation(players, num_episodes=cfg["SIMULATION"].getint("n"))
    print(winners)
elif cfg["GENERAL"]["MODE"] == "PLAY":
    players = []
    for p in cfg["PLAY"]["players"].split("\n"):
        players.append(Player.create_player(cfg[p]))
    GUI.play(BitBoard(players))