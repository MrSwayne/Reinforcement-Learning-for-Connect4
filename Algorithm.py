from abc import abstractmethod
from copy import deepcopy
import random
import math
import csv
import os

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

    path = 'state_values.csv'

    def __init__(self, train = False, duration = None, depth = None, n = None, e = 0.5, g = 0.5, a = 0.8):
        super().__init__()
        self.e = e
        self.duration = duration
        self.depth = depth
        self.n = n
        self.a = a
        self.end = None
        self.g = g
        self.value_function = {}
        self.policy_function = {}
        self.train = train

        self.num_new_states = 0
        if not duration and not depth and not n:
            self.n = 250

    def should_continue(self):
        if self.duration:
            if not self.end:
                self.end = datetime.now() + self.duration
                return True
            else:
                return datetime.now() < self.end

        if self.n:
            return self.current_n < self.n

        return False


    def get_move(self, state, player):
        self.end = None
        self.current_n = 0

        #Create game tree
        self.root = Node(parent=None, state=state, player=player, prev_action=-1)
      #  self.add_to_table(self.root)

        #Based on initial conditions like time per turn, or X amount of simulations etc.
        while self.should_continue():
            self.current_n += 1

            #Selection
            node = self.select_node()

            #Expansion
            if not node.state.game_over:
                self.expand(node)

            #Simulation
            terminal_state = self.simulation(node)

            #Backpropagation
            self.backpropagate(node, self.reward(terminal_state))


      #  prob_vector = []
      #  for child in self.root.children:
        best_child = self.get_best_child(self.root)
       # self.root.print()
      #  print(best_child)
      #  time.sleep(3)
        return best_child.state.get_last_move()

    def simulation(self, node):
        return self.rollout_policy(node.state)


    def update_value(self, node):

        score = node.score / node.visit_count
        while node.parent is not None:
            state = node.get_state()
            parent_state = node.parent.get_state()

            if state not in self.value_function:
                self.add_to_table(node)
            if parent_state not in self.value_function:
                self.add_to_table(node.parent)

            self.value_function[parent_state] = self.value_function[parent_state] + self.a * (score + (self.g * self.value_function[state]) - self.value_function[parent_state])
            node = node.parent



    def reward(self, state):
        check_win = state.check_win()

        if int(check_win) < 0:
            return 0
        elif int(check_win) == 0:
            return 0.5
        elif check_win == self.root.player:
            return 1
        else:
            return -1

    def add_to_table(self, node):
        state = node.get_state()
        if state not in self.value_function:
            val = 0
            if node.visit_count == 0:
                val = self.reward(node.state)
            else:
                val = node.score / node.visit_count
            self.value_function[state] = val ##self.reward(node.state)
            self.num_new_states += 1
        else:
            pass

    def create_node(self, parent, action):
        temp_board = deepcopy(parent.state)
        temp_board.place(action)
        node = (Node(parent=parent, state=temp_board, player=parent.player, prev_action=action, depth=parent.depth + 1))
        return node

    def backpropagate(self, node, reward):
        while node is not None:
            node.visit_count += 1
            node.score += reward
        #    self.update_value(node)
            node = node.parent

    def expand(self, node):
        for action in node.state.get_actions():
            child = self.create_node(node, action)
            node.children.append(child)

    def UCB(self, node):
        pvc = node.parent.visit_count
        cvc = node.visit_count
        cs = node.score

        if cvc == 0:
            return float('inf')

        return (cs / cvc + ( self.e * math.sqrt(math.log(pvc) / cvc)))

    def rollout_policy(self, state):
        temp_state = deepcopy(state)
        while not temp_state.game_over:
            actions = temp_state.get_actions()
            if len(temp_state.get_actions()) > 0:
                temp_state.place(random.choice(actions))
            else:
                break
        return temp_state

    def get_best_child(self, node):
        max_score = float('-inf')
        best_child = node

        for child in node.children:
            child_score = self.UCB(child)

            if child_score > max_score:
                max_score = child_score
                best_child = child
        return best_child

    def select_node(self):
        node = self.root

        #Go until leaf node
        while (len(node.children) != 0):
            node = self.get_best_child(node)
        return node


class Node:
    def __init__(self, parent, state, player, prev_action, depth=0):
        self.children = []
        self.parent = parent
        self.visit_count = 0
        self.score = 0
        self.state = state
        self.player = player
        self.prev_action = prev_action
        self.depth = depth
        self.tag = str(depth) + "_" + str(prev_action)

    def get_state(self):
        boards = str(bin(self.state.get_state(self.player)))
        for p in self.state.players:
            if p is not self.player:
                boards += " " + (str(bin(self.state.get_state(p))))
        return boards

    def __repr__(self):
        return "{" + str(self.tag) + "," + str(self.score) + "," + str(self.visit_count) + "}"

    def print(self):
        print(repr(self), "->", self.children)
        for child in self.children:
            child.print()



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