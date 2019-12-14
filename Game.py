import pygame
from copy import deepcopy
from ConnectBoard import *
from BitBoard import *
from TicBoard import *
from Player import *
import Algorithm as algo
from keras.utils import to_categorical
import time
import os
import csv
path = "state_action.csv"

def create_board(players):
    return BitBoard(players)

def load_data():
    table = {}
    if not os.path.isfile(path):
        f = open(path, "w+")
        f.close()

    with open(path, 'r' ) as csvfile:
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

def save_data( table):
        if not os.path.isfile(path):
            f = open(path, "r+")
            f.close()
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(["state","mask", "action"])
            for state, action in table.items():
                writer.writerow([state[0], state[1], action])

class _State:
    def __init__(self, player_state, mask):
        self.player_state = player_state
        self.mask = mask

def simulation(players, num_episodes=10, _print=False):
    completed_games = []

    new_states = 0
    policy_table = load_data()

    state = create_board(players)

    for i in range(num_episodes):
        print("Game: ", i, end="\t")

        state.reset()
        total_actions = len(state.get_actions())

        last_action = -1
        while not state.game_over:
            player = state.get_player_turn()
            action = player.get_choice(state)

            player_state, state_mask = state.get_state(player)
           # old_states = np.vectorize(np.binary_repr)(np.array([[player_state, state_mask]]), 64)
            old_states = np.array([[player_state, state_mask]])
            state.place(action)

            if isinstance(player.algorithm, algo.MCTS):

                player_state, state_mask = state.get_state(player)

                if player.neural_net is not None:
                    print("MCTS: ", action, "\tNN:", player.neural_net.model.predict(old_states))
                  #  action_vector = np.array([to_categorical(action, num_classes=total_actions)])
                    #states = np.vectorize(np.binary_repr)(np.array([[player_state, state_mask]]), 64)
                    states = np.array([[player_state, state_mask]])
                    # neural_action = np.argmax(player.neural_net.predict(states))

              #      action_vector[action]
                    player.neural_net.learn(state=old_states, next_state=states, action=action,reward= player.algorithm.reward(state))

            winner = state.check_win()

            if _print:
                state.print()

        completed_games.append(deepcopy(state))

        for p in players:
            if isinstance(p.algorithm, algo.MCTS):
                new_states = p.algorithm.num_new_states


        if isinstance(winner, Player):
                print(winner, "(", winner.algorithm, ")", " Won!")
        elif isinstance(winner, Player):
            print(winner, " (Human) Won!")
        else:
            print("DRAW!")

    save_data(policy_table)
    for player in players:
        if player.neural_net is not None:
            player.neural_net.save()

    return completed_games, new_states

def manual(players, sequence):
    completed_games = []
    state = create_board(players)
    bools = state.placeSequence(sequence)
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
                print(pygame.mouse.get_pos())

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
    for state in completed_games:
        state.print()

        winner = state.check_win()
        if winner in winners:
            winners[winner] += 1
        else:
            winners[winner] = 1
        print(winner)

    print("out of {0} games".format(len(completed_games)))
    print(winners)
