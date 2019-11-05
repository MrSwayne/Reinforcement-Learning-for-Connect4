from abc import abstractmethod
from copy import deepcopy
import random
import math
import csv

import time
import random
from copy import deepcopy
import math
from datetime import datetime, timedelta

class Algorithm():

    algorithms = ["MINIMAX", "MCTS", "RANDOM"]

    def __init__(self):
        pass

    @abstractmethod
    def get_move(self, state, player):
        pass

class MCTS(Algorithm):

    def __init__(self, train=False, duration = None, depth = None, n = None, e = 0.5, g = 0.5, a = 0.8):
        super().__init__()
        self.e = e
        self.duration = duration
        self.depth = depth
        self.n = n
        self.a = a
        self.end = None
        self.g = g
        self.table = {}

        if train:
            self.load_data()

    def load_data(self):
        self.table = {}
        with open('state_values.csv', 'r+' ) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')

            headers = True
            for row in reader:
                if headers:
                    headers = False
                    continue
                self.table[row[0]] = float(row[1])

    def save_data(self):
        if self.table:
            with open('state_values.csv', 'w+', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(["state", "value"])
                for state, value in self.table.items():
                    writer.writerow([state, value])

    def should_continue(self):
        if self.duration:
            if not self.end:
                self.end = datetime.now() + self.duration
                return True
            else:
                return datetime.now() < self.end

        if self.n:
            return self.root.visit_count < self.n

        return False

    def get_move(self, state, player):
        self.end = None
        self.game_tree = Tree(player=player, state=state)
        self.root = self.game_tree.root


        if self.root.get_state() not in self.table:
            self.table[self.root.get_state()] = 0

        node = None
        while self.should_continue():
            node = self.select_node()
            if not node.state.game_over:
                self.expand(node)

            reward = self.simulation(node)

            self.backpropagate(node, reward)

        node = self.get_best_child(self.root)
        if node.get_state() in self.table:
            self.update_value(self.root.get_state(), node.get_state(), node.score / node.visit_count)
        else:
            self.table[node.get_state()] = node.score / node.visit_count

        return node.state.get_last_move()



    def update_value(self, state, next_state, score):
        self.table[state] = self.table[state] + self.a * (score +  (self.g * self.table[next_state]) - self.table[state] )

    def simulation(self, node):
        state = deepcopy(node.state)

        terminal_state = self.rollout_policy(state)
        return self.reward(terminal_state)


    def reward(self, state):
        check_win = state.check_win()
        if check_win == self.game_tree.root.player:
            return 1
        elif int(check_win) == 0:
            return 0.5
        elif int(check_win) < 0:
            return 0
        else:
            return -1

    def backpropagate(self, node, reward):
        while node is not None:
            node.visit_count += 1
            node.score += reward
            node = node.parent

    def expand(self, node):
        children = node.get_child_states()


        for child in children:
            if node.get_state() in self.table:
                node.score = self.table[node.get_state()]
                node.visit_count += 1
            node.children.append(child)

    def UCB(self, node):
        pvc = node.parent.visit_count
        cvc = node.visit_count
        cs = node.score

        if cvc == 0:
            return float('inf')

        return (cs / cvc + ( self.e * math.sqrt(math.log(pvc) / cvc)))

    def rollout_policy(self, state):
        while not state.game_over:
            actions = state.get_actions()
            if len(state.get_actions()) > 0:
                state.place(random.choice(actions))
        return state

    def get_best_child(self, node):
        max_score = float('-inf')
        best_child = None
        for child in node.children:

            child_score = self.UCB(child)

            if child_score > max_score:
                max_score = child_score
                best_child = child
        return best_child

    def select_node(self):
        node = self.root
        #Go until leaf node

        count = 0
        while (len(node.children) != 0 and not node.state.game_over):
            node = self.get_best_child(node)
        return node


class Node:
    def __init__(self, parent, state, player, prev_action):
        self.children = []
        self.parent = parent
        self.visit_count = 0
        self.score = 0
        self.state = state
        self.player = player
        self.prev_action = prev_action

    def get_state(self):
        return self.state.get_state(self.player)

    def get_child_states(self):
        states = []
        for action in self.state.get_actions():
            temp_board = deepcopy(self.state)
            temp_board.place(action)
            states.append(Node(parent=self, state=temp_board, player = self.player, prev_action=action))
        return states

class Tree:
    def __init__(self, player, state):
        self.root = Node(player=player, state=state, parent=None, prev_action= -1)



class Random(Algorithm):

    def __init__(self):
        super().__init__()

    def get_move(self, state, player):
        return random.choice(state.get_actions())



class Minimax(Algorithm):

    def __init__(self, max_depth = 4):
        super().__init__()
        self.depth = max_depth

    def get_move(self, state, player):
        self.player = player
        return self.minimax(state)

    def minimax(self, board, depth=0):

        winner = board.check_win()
        if winner == self.player:
            return 1
        elif winner in board.players:
            return -1
        elif int(winner) == 0:
            return 0

        if depth == self.depth:
                return 0

        max_score = float('-inf')

        actions = board.get_actions()

        choices = []
        for action in actions:
            score = float('-inf')
            new_board = deepcopy(board)

            new_board.place(action)
            score += self.minimax(new_board, depth + 1)

            if score == max_score:
                choices.append(action)

            elif score > max_score:
                max_score = score
                choices.clear()
                choices.append(action)

        if len(choices) > 0 and depth == 0:
            return random.choice(choices)
        return max_score