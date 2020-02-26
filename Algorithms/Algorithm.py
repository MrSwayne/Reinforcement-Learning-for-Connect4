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
    def get_name(self):
        pass

    @abstractmethod
    def get_memory(self):
        return {}

    @abstractmethod
    def clear_memory(self):
        pass

    @abstractmethod
    def set_memory(self, data):
        pass

    @abstractmethod
    def load_memory(self):
        pass

    @abstractmethod
    def get_values(self):
        return []

from Core.IO import IO
class Tree:

    @staticmethod
    def create_tree(state, data):
        root = Node(parent=None, state=state, player=state.get_player_turn(), prev_action=-1, depth=0, data=data)
        return root
class Node:

    def create_children(self):
        for action in self.state.get_actions():

            _state = deepcopy(self.state)
            _state.place(action)
            player = _state.get_player_turn()
            child = Node(parent=self, state=_state, player=player, prev_action=action, depth= self.depth + 1, data=self.data)
            self.children.append(child)

            if self.best_child is None or child.V > self.best_child.V:
                self.best_child = child
            if self.worst_child is None or child.V < self.worst_child.V:
                self.worst_child = child

    @property
    def V(self):
        return self._V

    @property
    def visit_count(self):
        return self._visits

    @property
    def score(self):
        return self._score

    @V.setter
    def V(self, value):
        self._V = value


        self.data[self.get_state()] = (self.score, self.V, self.visit_count)

        if self.parent is not None:
            if self._V > self.parent.best_child.V:
                self.parent.best_child = self
            if self._V < self.parent.best_child.V:
                self.parent.worst_child = self

    @visit_count.setter
    def visit_count(self, value):
        self._visits = value

        self.data[self.get_state()] = (self.score, self.V, self.visit_count)

    @score.setter
    def score(self, value):
        self._score = value

        self.data[self.get_state()] = (self.score, self.V, self.visit_count)

    def __init__(self, parent, state, player, prev_action, depth=0, data = {}):
        self.data = data
        self.children = []
        self.parent = parent
        self._visits = 0
        self._score = 0

        self.state = state
        self.player = player
        self.prev_action = prev_action
        self.depth = depth

        self.best_child = None
        self.worst_child = None
        self._V = 0.5
        if state is not None:
            if state.game_over:
                self._V = 0
            self.total_actions = state.get_actions()

        if self.get_state() in self.data:
            (self._score, self._V, self._visits) = self.data[self.get_state()]


    def get_state(self):
        if self.state is None:
            return None
        return self.state.get_state()


    def __repr__(self):
        return str(self.get_state())

    def __str__(self):
        return str((self.score, self.V, self.visit_count))

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