from Core.Logger import LOGGER
import configparser

cfg = configparser.ConfigParser()
cfg.read("config.ini")

log_path = cfg["IO"]["log_path"] + cfg["LOGGING"].get("file_name", "log.out")
LOGGER.filename = log_path
logger = LOGGER.attach(__name__)

from Core.IO import IO
IO.verify(cfg["IO"]["log_path"])
print("Logging to: ", log_path)

#logger.info({section: dict(cfg[section]) for section in cfg.sections()})
from Player import *
import Game as Game

from GUI import GameGUI as GUI
from Algorithms import *
from Boards import *

players = []
SEED = cfg["GENERAL"].getint("seed", 10)
random.seed(SEED)
logger.info("SEED: " + str(SEED))
mode = cfg["GENERAL"]["MODE"].upper()

max_explore = cfg["GENERAL"].getboolean("max_explore", False)
logger.info("MODE: " + mode)
logger.info("Max Explore: " + str(max_explore))

board = get_board(cfg["GENERAL"].get("board", ConnectBoard))
if mode == "TRAIN":
    episodes = cfg["TRAIN"].getint("episodes")
    batch = cfg["TRAIN"].getint("batch")
    tournament_games = cfg["TRAIN"].getint("tournament_games")

    for p in cfg["TRAIN"]["players"].split(","):
        player = Player.create_player(cfg[p])
        players.append(player)

    enemy = Player.create_player(cfg[cfg["TRAIN"]["enemy"]])

    training_res, tournament_res = Game.experiment(board, players, enemy, episodes, batch, tournament_games, max_explore)

elif mode == "SIMULATION":
    players = []

    iter = []
    for p in cfg["SIMULATION"]["players"].split(","):
        print(p)
        player = Player.create_player(cfg[p])
        players.append(player)
        player.set_learning(cfg["SIMULATION"].getboolean("learn", False))
        if cfg["SIMULATION"].get("iterative", None) == p:
            iter.append(player)
    if len(iter) > 0:

        path = iter[0].algorithm.memory
        head, tail = os.path.split(path)
        for file in sorted(IO.list(head), key=len):
            if tail + "_" in file:
                logger.info("found " + str(file))
                f, ext = os.path.splitext(file)
                iter[0].algorithm.memory = head + "/" + f
                iter[0].algorithm.load_memory()

                completed_games, winners, avg_states = Game.simulation(board, players, num_episodes=cfg["SIMULATION"].getint(
                    "episodes"), debug=False)
                print()
                print(winners, "\t", avg_states)
                print()

    else:
        completed_games, winners, avg_states = Game.simulation(board, players, num_episodes=cfg["SIMULATION"].getint("episodes"), debug=False)

        print()
        print(winners, "\t", avg_states)

        if cfg["SIMULATION"].getboolean("train", False):
            for p in players:
                if isinstance(p, Bot):
                    p.save("_s")
        GUI.draw(completed_games)

elif mode == "PLAY":
    players = []
    for p in cfg["PLAY"]["players"].split(","):
        players.append(Player.create_player(cfg[p]))
    GUI.play(BitBoard(players))