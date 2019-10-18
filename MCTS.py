from BitBoard import *
import random
import copy
import math
class Node:

    def __init__(self, player, state, action = -1, e = 1, depth = 0, max_depth = 4):
        self.children = []
        self.num_wins = 0
        self.state = state
        self.visit_count = 0
        self.e = e
        self.player = player
        self.prev_action = action
        self.depth = depth

        if self.depth == max_depth:
            return
        else:
            self.expand()


    def add_child(self, node):
        self.children.append(node)

    def expand(self):
        for action in self.state.get_actions():
            temp_state = copy.deepcopy(self.state)
            temp_state.place(action)

            node = Node(self.player, temp_state, action, e= self.e, depth= self.depth +1)
            self.children.append(node)

            node.simulate(1)
            self.visit_count += 1


    def has_children(self):
        return len(self.children)


    def reward(self, state):
        check_win = state.check_win()
        if check_win == self.player:
            return  1
        elif int(check_win) == 0:
            return 0.5
        elif int(check_win) < 0:
            return  0
        else:
            return -1

    def select_child(self):
        self.visit_count += 1
        max = 0
        best_child = None
        for child in self.children:

            if child.visit_count == 0:
                child.expand()

            ucb1 = (child.num_wins / child.visit_count + (self.e * math.sqrt(math.log(self.visit_count) / child.visit_count)))


            if ucb1 >= max:
                max = ucb1
                best_child = child

        return best_child


    def play_game(self, state):
        temp_state = copy.deepcopy(state)
        while not temp_state.game_over:
            actions = temp_state.get_actions()

            if len(actions) > 0:
                temp_state.place(random.choice(actions))
            else:
                break
        return temp_state


    def simulate(self, n = 10):

        for i in range(n):
            best_child = self.select_child()

            if best_child is not None:
                reward = self.reward(self.play_game(best_child.state))

                if reward == 1:
                    best_child.num_wins += 1
                    self.num_wins += 1

                best_child.visit_count += 1







