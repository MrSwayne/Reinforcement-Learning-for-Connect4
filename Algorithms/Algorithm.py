from abc import abstractmethod
import random
from copy import deepcopy
import math
from datetime import datetime, timedelta

class Algorithm():

    def __init__(self):
        self.learning = True
        pass

    @abstractmethod
    def get_move(self, state):
        pass

    @abstractmethod
    def load_data(self, path):
        pass

    @abstractmethod
    def save_data(self, path):
        pass

    @abstractmethod
    def get_name(self):
        pass

    def clear_memory(self):
        pass

    @abstractmethod
    def get_values(self):
        pass

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

        self.best_child = None
        self.worst_child = None
        self.tag = str(depth) + "_" + str(prev_action)

        if state is not None and state.game_over:
            self.V = 0
        else:
            self.V = 0.5

    def get_state(self):
        if self.state is None:
            return None
        return self.state.get_state()

    def __repr__(self):
        return "{" + str(self.depth) + "_" + str(self.prev_action) + "," + str(self.score) + "S," + (str(round(self.V, 4))) + "V," + str(
            self.visit_count) + "N," + str(self.player) + "}"

    def print(self, backwards=False):

        if backwards:
            temp_node = self
            list = []
            while (temp_node is not None):
                list.append(temp_node)
                temp_node = temp_node.parent

            print(list)
        else:
            print(repr(self), "->", self.children)
            for child in self.children:
                child.print()


class Random(Algorithm):

    def __init__(self):
        super().__init__()

    def get_move(self, state):
        choice = random.choice(state.get_actions())

        return choice

    def get_name(self):
        return "Random"