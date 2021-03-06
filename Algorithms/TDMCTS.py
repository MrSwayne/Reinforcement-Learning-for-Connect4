from Algorithms.MCTS import *
import os
import csv


class MCTS_TDUCT3(MCTS):

    def get_name(self):
        return "MCTS_TDUCT"

    def reward(self, node, state):
        if not state.game_over:
            return 0
        check_win = state.winner

        if int(check_win) == -1:
            return 0
        if int(check_win) == int(node.player):
            return self.MIN_REWARD
        elif int(check_win) == 0:
            return 0
        else:
            return self.MAX_REWARD


    def tree_value(self, node):
        if node.visit_count == 0:
            return float("inf")
        else:
            return node.V + (self.e * math.sqrt(math.log(node.parent.visit_count) / node.visit_count))
    def tree_policy(self, node):
        max_score = float('-inf')

        best_children = []

        for child in node.children:
             #   logger.debug("Max exploration set. " + str(child.prev_action) + " " + str(score))
                #normalised_score = (child.V - node.best_child.V) / ((node.best_child.V - node.worst_child.V) + 1)
               # print(normalised_score)
              #  score = normalised_score + self.e * math.sqrt(math.log(pvc) / cvc)

            score = self.tree_value(child)


            if score > max_score:
                best_children = []
                max_score = score
            if score >= max_score:
                best_children.append(child)

        return random.choice(best_children)

    def select_node(self):
        node = super().select_node()
        return node

    def child_policy(self, node):
        highest_val = float("-inf")

        best_children = []

        if self.max_explore:
            min_visits = float("inf")

            for child in node.children:
                if child.visit_count < min_visits:
                    min_visits = child.visit_count
                    best_children = []
                if child.visit_count <= min_visits:
                    best_children.append(child)
        else:

            return self.tree_policy(node)

            #for child in node.children:
            '''
                if child.V > highest_val:
                    best_children = []
                    highest_val = child.V
                if child.V >= highest_val:
                    best_children.append(child)
            '''
        return random.choice(best_children)



    def backpropagate(self, node, reward, num_steps):

        reward *= (self.gamma ** (num_steps))

        alpha = max(1 / (node.visit_count + 1), self.a)
        node.V = node.V + alpha * (reward - node.V)

        while node is not None:
            if reward > 0:
                node.score += 1
            reward *= -1
            node.visit_count += 1
            if node.parent is not None:

                target = -(self.reward(node.parent, node.parent.state) + self.gamma * node.V)
                alpha = max(1 / (node.parent.visit_count), self.a)

                node.parent.V = node.parent.V + alpha * (target - node.parent.V)
            node = node.parent