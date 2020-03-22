from BitBoard import *
from Algorithms.MCTS import *
import time
from Core import LOGGER


def create_board(players):
    return BitBoard(players)

logger = LOGGER.attach(__name__)
def experiment(players, enemy, episodes = 500, batch= 100, tournament_games = 100):

    tournament_number = 1
    training_results = []
    tournament_results = []
    i = 0
    _p = None
    for p in players:
        if _p is None:
            _p = p
        else:
            if isinstance(type(_p.algorithm), type(p.algorithm)):
                p.algorithm.set_memory(_p.algorithm.get_memory())

    while i < episodes:
        #Train
        if i != 0:
            for p in players:
                p.set_learning(True)

            print("Training ", i, "-", i + batch - 1)
            logger.info("Training " + str(i) + "-" + str(i + batch - 1))
            t0 = time.clock()

            print(players)
            logger.info("Training: " + str(players))
            completed_games, winners, avg_moves = simulation(players, num_episodes=batch, debug=False)
            t1 = time.clock()
            print("Training ", batch, " games = ", t1-t0, " seconds")
            logger.info("Training " + str(batch) + " games = " + str(t1-t0) + " seconds")
            logger.info(str(winners) + " " + str(avg_moves))
            training_results.append((completed_games, winners, avg_moves))
            i += batch
            players[0].save("_" + str(i - 1))
        else:
            i += 1

        tournament_players = [players[0], enemy]
        #Tournament
        print("Tournament ", tournament_number, "\t", tournament_players)

        t0 = time.clock()
        for p in tournament_players:
            p.set_learning(False)

        logger.info("Tournament: " + str(players))
        completed_games, winners, avg_moves = simulation(tournament_players, tournament_games)

        t1 = time.clock()
        print("Tournament ", tournament_games, " games = ", t1 - t0, " seconds")
        logger.info("Tournament " + str(tournament_games) + " games = " + str(t1 - t0) + " seconds")
        print(winners)
        logger.info(winners)
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

        print(winner, " ", len(state.moves), " ", winners, end="\t\r")
        logger.info("Game " + str(i+1) + " " + str(winner) + " " + str(winners))
        logger.info("End state: " + str(state.get_state()) + str(state.moves))
        completed_games.append(deepcopy(state))

    if num_episodes > 0:
        avg /= num_episodes
    print()

    logger.debug("Completed Simulation of " + str(num_episodes))
    for game in completed_games:
        logger.debug(str(game.get_state()) + " : " + str(game.winner))
    return completed_games, winners, avg

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
