from Algorithms.MCTS import *

class MCTS_UCT(MCTS):

    def __init__(self,memory,  duration=None, depth=None, n=2000, e=1.414, g=0.9, l=1, debug=False):
        super().__init__(memory, duration, depth, n, e, g, l, debug)

        self.MAX_REWARD = 1
        self.MIN_REWARD = -1

    def get_name(self):
        return "MCTS_UCT"

    def reward(self, node, state):
        if not state.game_over:
            return 0
        check_win = state.winner

        if(int(check_win) == int(node.player)):
            return self.MIN_REWARD
        elif(int(check_win) < 0):
            return self.MIN_REWARD
        elif(int(check_win) == 0):
            return (self.MAX_REWARD + self.MIN_REWARD) / 2
        else:
            return self.MAX_REWARD

    def select_node(self):
        node = super().select_node()
        return node

    def child_policy(self, node):
        highest_val = float("-inf")
        best_child = None

        for child in node.children:
            if child.score >= highest_val:
                highest_val = child.score
                best_child = child
        return best_child

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
                score = (cs / cvc) + 2 * (self.e * math.sqrt(2 * math.log(pvc) / cvc))

            if score > max_score:
                best_children = []
                max_score = score
            if score >= max_score:
                best_children.append(child)

        return random.choice(best_children)

    def backpropagate(self, node, reward, num_steps):

        player = node.player
        while node is not None:

            if reward >= 1:
                node.score += 1
            reward *= -1

            node.visit_count += 1

            node = node.parent
