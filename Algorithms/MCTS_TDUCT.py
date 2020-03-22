from Algorithms.MCTS import *
import os
import csv

class MCTS_TDUCT(MCTS):

    def get_name(self):
        return "MCTS_TDUCT"

    def reward(self, node, state):
        if not state.game_over:
            return 0
        else:
            check_win = state.winner

        if int(check_win) == -1:
            return 0
        if int(check_win) == int(node.player):
            return self.MIN_REWARD
        elif int(check_win) == 0:
            return (self.MAX_REWARD + self.MIN_REWARD) / 2
        else:
            return self.MAX_REWARD

    def tree_policy(self, node):
        max_score = float('-inf')

        best_children = []

        for child in node.children:
            pvc = node.visit_count
            cvc = child.visit_count
            cs = child.score

            if cvc == 0:
                score = float('inf')

            else:
                #normalised_score = (child.V - node.best_child.V) / ((node.best_child.V - node.worst_child.V) + 1)
               # print(normalised_score)
              #  score = normalised_score + self.e * math.sqrt(math.log(pvc) / cvc)

                score = child.V + (self.e * math.sqrt( math.log(pvc) / (cvc + 1)))
                #print(score, "....", normalised_score, "......", child.V, "-", child.visit_count)
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
        best_child = None

        for child in node.children:

            if child.state.game_over:
                return child

            if child.V >= highest_val:
                highest_val = child.V
                best_child = child
        return best_child

    def backpropagate(self, node, reward, num_steps):
        reward *= (self.gamma ** (num_steps))

        target = reward - node.V

        while node is not None:

            if target >= 0:
                node.score += 1
            node.visit_count += 1
            alpha = max(1 / (1 + node.visit_count), 0.005)
            node.V = node.V + alpha * target - node.V

            node = node.parent