import Algorithms
from Boards.BitBoard import *
from Algorithms.MCTS import *
import time
from Core import LOGGER



logger = LOGGER.attach(__name__)
def experiment(board, players, enemy, episodes = 500, batch= 100, tournament_games = 100, max_explore=False):

    tournament_number = 1
    training_results = []
    tournament_results = []
    i = 0
    _p = None

    for p in players:
        if _p is None:
            _p = p
        else:
            if(type(p.algorithm) == type(p.algorithm)):
                logger.info("Setting : " + str(p) + " to the memory of : " + str(_p))
                p.algorithm.set_memory(_p.algorithm.get_memory())
    try:
        while i < episodes:
            #Train
            if i != 0:

                for p in players:
                    p.set_learning(True)

                print("Training ", i, "-", i + batch - 1)
                logger.info("Training " + str(i) + "-" + str(i + batch - 1))
                t0 = time.process_time()

                print(players)
                logger.info("Training: " + str(players))
                completed_games, winners, avg_moves = simulation(board, players, num_episodes=batch, debug=False, max_explore=max_explore)
                t1 = time.process_time()
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

            t0 = time.process_time()
            for p in tournament_players:
                p.set_learning(False)

            logger.info("Tournament: " + str(players))
            completed_games, winners, avg_moves = simulation(board, tournament_players, tournament_games)

            t1 = time.process_time()

            print()
            print("Tournament ", tournament_games, " games = ", t1 - t0, " seconds")
            logger.info("Tournament " + str(tournament_games) + " games = " + str(t1 - t0) + " seconds")
            print(winners, " ", avg_moves)
            logger.info(winners)

            print()
            tournament_number += 1
            tournament_results.append((completed_games, winners, avg_moves))
    except Exception as e :
        print(e)
        logger.error(e)
    finally:
        print("--\nTraining--\n")
        logger.info("-------Training results--------")

        num = 0
        for completed_games, winners, avg_moves in training_results:
            print(winners, "\t", avg_moves)
            logger.info(str(num + 1) + str(winners) + " " + str(avg_moves))
            print()
            num += 1

        print("--\nTournament--\n")
        logger.info("-------Tournament results--------")

        num = 0
        for completed_games, winners, avg_moves in tournament_results:
            avg = 0

            print(winners, "\t", avg_moves)
            logger.info(str(num + 1) + " " + str(winners) + " " + str(avg_moves))
            num += 1

    return training_results, tournament_results

def simulation(board, players, num_episodes=10, table = {}, debug=False, max_explore=False):
    completed_games = []

    state = board(players)
    winners = {}
    prev_total_states = 0

    avg = 0
    print(players)
    for i in range(num_episodes):
        print("Game ", (i+1), end = " - " )
        state.reset()
        winner = None

        while not state.game_over:

            if max_explore:
                if len(state.moves) < 1:
                    explore = True
                else:
                    explore = False

                for p in players:
                    if isinstance(p.algorithm, Algorithms.MCTS):
                        p.algorithm.max_exploration(explore)

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

    logger.info("Completed Simulation of " + str(num_episodes))

    j = 0
    for game in completed_games:
        logger.info(str(j+1) + ". " + str(game.get_state()) + " : " + str(game.winner) + " : " +  str(game.moves) )
        j += 1
    return completed_games, winners, avg

def manual(board, players, sequence):
    completed_games = []
    state = board(players)
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
