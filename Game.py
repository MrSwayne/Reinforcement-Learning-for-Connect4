import pygame
from copy import deepcopy
from ConnectBoard import *
from BitBoard import *
from TicBoard import *
from Player import *
import Algorithm as algo
#from keras.utils import to_categorical
import time
import os
import csv
import pandas

tree_path = "tree_data.csv"
value_path = "values.csv"


def create_board(players):
    return BitBoard(players)


def load_tree_data():
    table = {}
    if not os.path.isfile(tree_path):
        f = open(tree_path, "w+")
        f.close()

    with open(tree_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        headers = True
        for row in reader:
            if headers:
                headers = False
                continue

            if len(row) == 4:
                try:
                    table[int(row[0]), int(row[1])] = (float(row[2]), float(row[3]))
                except:
                    continue
    return table


def load_value_function():
    table = {}
    if not os.path.isfile(value_path):
        f = open(value_path, "w+")
        f.close()

    with open(value_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        headers = True
        for row in reader:
            if headers:
                headers = False
                continue

            if len(row) == 3:
                try:
                    table[row[0], row[1]] = float(row[2])
                except:
                    continue
    return table


def save_value_function(table):
    if not os.path.isfile(tree_path):
        f = open(value_path, "r+")
        f.close()
    with open(value_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["state", "mask", "value"])
        for state, value in table.items():
            writer.writerow([state[0], state[1], value])


def save_tree_data(table):
    if not os.path.isfile(tree_path):
        f = open(tree_path, "r+")
        f.close()
    with open(tree_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["state", "mask", "score", "visit count"])
        for state, node in table.items():
            writer.writerow([state[0], state[1], node[0], node[1]])


class _State:
    def __init__(self, player_state, mask):
        self.player_state = player_state
        self.mask = mask


def simulation(players, num_episodes=10, _print=False):
    completed_games = []

    state = create_board(players)

    tree_data = load_tree_data()
    winners = {}
    for p in players:
        winners[p] = 0
        if isinstance(p.algorithm, algo.MCTS):
            if p.algorithm.memory:
                p.algorithm.tree_data = tree_data


    alpha = 0.8
    gamma = 0.9

    for i in range(num_episodes):

        print("Game: ", i + 1)

        state.reset()

        winner = None
        while not state.game_over:

            if _print:
                state.print()

            player = state.get_player_turn()

            action = player.get_choice(state)

      #      if isinstance(player.algorithm, algo.MCTS):
      #          print(player, "\t",player.algorithm.root, "->", player.algorithm.root.children)

            player_state, state_mask = state.get_state(player)
            # old_states = np.vectorize(np.binary_repr)(np.array([[player_state, state_mask]]), 64)
            #  old_states = np.array([[player_state, state_mask]])

            #  action = np.argmax(action_vector)
            state.place(action)
            winner = state.check_win()




            '''
            for p in players:
                
                if isinstance(p.algorithm, algo.MCTS):
                    reward = get_reward(p, winner)
                    visited_states[p].append(state.get_state(p))

                    t_temp = time_step
                    while t_temp > 0:
                        s = visited_states[p][t_temp]
                        prev_s = visited_states[p][t_temp - 1]
                        if s not in value_function:
                            if state.game_over:
                                value_function[s] = reward
                            else:
                                value_function[s] = 0.5
                        value_function[prev_s] = value_function[prev_s] + alpha * (reward + gamma * value_function[s] - value_function[prev_s])
                        t_temp -= 1
            '''
            if isinstance(player.algorithm, algo.MCTS):
                player_state, state_mask = state.get_state(player)

                if player.neural_net is not None:
                    pass
                    #  action_vector = np.array([to_categorical(action, num_classes=total_actions)])
                    # states = np.vectorize(np.binary_repr)(np.array([[player_state, state_mask]]), 64)
                    #         states = np.array([[player_state, state_mask]])
                    # neural_action = np.argmax(player.neural_net.predict(states))

                    #      action_vector[action]
                    '''
                    print("AV->", action_vector)
                    print("P-->", player.neural_net.model.predict(states))
                    player.neural_net.learn(X = old_states, Y= np.array([action_vector]))
                    print("P-->", player.neural_net.model.predict(states))
                    print()
                    '''

        if winner in winners:
            winners[winner] += 1
        if _print:
            state.print()

        if ((i + 1) % 20 == 0 or i == num_episodes - 1):
            save_tree_data(tree_data)
            '''
            best_player = None
            best_count = 0
            for winner, count in winners.items():
                if isinstance(winner.algorithm, algo.MCTS):
                    if count >= best_count:
                        best_player = winner
                        best_count = count

            if best_player is not None and not 0:
                print("saving: ", best_player)
                save_tree_data(best_player.algorithm.tree_data)
            for player in players:
                if player == best_player:
                    continue
                if isinstance(winner.algorithm, algo.MCTS) and player.algorithm.memory:
                    player.algorithm.tree_data = load_tree_data()
            '''
        completed_games.append(deepcopy(state))

        if (winner == 0):
            print("DRAW!")
        else:
            print(winner, " Won!")

    return completed_games, 0


def get_reward(player, winner):
    if int(winner) < 0:
        return 0
    elif int(winner) == 0:
        return 0.5
    elif winner == player:
        return 1
    else:
        return -1


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


def draw(states, width=1280, height=720):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    done = False

    player_colour_map = {0: (255, 255, 255)}

    players = states[0].get_players()
    for player in players:
        player_colour_map[player] = player.get_rgb()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                break
               # print(pygame.mouse.get_pos())

        state_offset_x = 0
        state_offset_y = 0

        count = 1
        for state in states:

            x_offset = 30 + state_offset_x
            y_offset = 30 + state_offset_y

            for r in range(state.rows):
                for c in range(state.cols):
                    #            for r in range(state.rows - 1, -1, -1):
                    #                for c in range(0, state.cols):
                    cell = state.get(r, c)

                    try:
                        colour = player_colour_map[cell]
                    except:
                        colour = player_colour_map[0]

                    pygame.draw.rect(screen, colour, pygame.Rect(x_offset, y_offset, 30, 30))
                    x_offset += 31
                x_offset = 30 + state_offset_x
                y_offset += 31
            state_offset_y = y_offset + 2

            if count % 3 == 0:
                state_offset_x += 260
                state_offset_y = 0

            count += 1

        pygame.display.flip()


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
