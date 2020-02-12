from Algorithms.MCTS_TDUCT import *

class MCTS_TDUCT2(MCTS_TDUCT):

    def get_name(self):
        return "MCTS_TDUCT2"

    def select_node(self):
        node = super().select_node()

        if node.get_state() not in self.tree_data:
            self.tree_data[node.get_state()] = (node.visit_count, node.score, node.V)

        return node

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

    def backpropagate(self, node, reward, num_steps):


        if node.state.game_over and 1 == 2:
            print(self.reward(node, node.state))
            node.state.print()
            print(node.player)
            print(node.state.check_win())
            print(node.parent.state.print())
            print(node.parent.player)
            print(self.reward(node.parent, node.state))

        reward *= self.gamma ** num_steps
        while node is not None:
            node.visit_count += 1

            if node.parent is not None:
                reward *= -self.gamma
                alpha = 1/ (1 + node.parent.visit_count)
               # node.parent.V = node.parent.V + alpha * (self.reward(node, node.state) + self.gamma * node.V - node.parent.V)
                node.parent.V = node.parent.V + alpha * (reward + self.gamma * node.V - node.parent.V)


                if node.V > node.parent.upper_bound:
                    node.parent.upper_bound = node.V
                if node.V < node.parent.lower_bound:
                    node.parent.lower_bound = node.V
                self.tree_data[node.get_state()] = (node.visit_count, node.score, node.V)

            node = node.parent