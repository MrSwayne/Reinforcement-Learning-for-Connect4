from Algorithms.MCTS import *

class MCTS_TDUCT(MCTS):

    def create_node(self, parent=None, action=-1, state=None, player=None):

        if parent is None:
            node = Node(parent=None, state=state, player=player, prev_action=action, depth=0)
        else:
            temp_board = deepcopy(parent.state)

            temp_board.place(action)
            player = temp_board.get_player_turn()
            node = (Node(parent=parent, state=temp_board, player=player, prev_action=action, depth=parent.depth + 1))

        _state = node.get_state()

        if _state in self.tree_data:
            node.visit_count, node.score, node.V = self.tree_data[_state]
        return node


    def get_name(self):
        return "MCTS_TDUCT"

    def reward(self, node, state):
        if not state.game_over:
            check_win = state.check_win()
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
                normalised_score = (child.V - node.upper_bound) / ((node.upper_bound - node.lower_bound) + 1)
                score = normalised_score + 2 * (self.e * math.sqrt(2 * math.log(pvc) / cvc))

            if score > max_score:
                best_children = []
                max_score = score
            if score >= max_score:
                best_children.append(child)

        return random.choice(best_children)

    def select_node(self):
        node = super().select_node()

        if node.get_state() not in self.tree_data:
            self.tree_data[node.get_state()] = (node.visit_count, node.score, node.V)

        return node

    def child_policy(self, node):
        highest_val = float("-inf")
        best_child = None

        for child in node.children:

            if child.V == 0:
                return child

            if child.V >= highest_val:
                highest_val = child.V
                best_child = child
        return best_child

    def backpropagate(self, node, reward, num_steps):

        td_error = (self.gamma ** (num_steps)) * reward - node.V

        while node is not None:
            td_error *= -1
            node.visit_count += 1

            alpha = 1 / node.visit_count
            node.V = node.V + alpha * (td_error) * self.gamma

            if node.parent is not None:
                if node.V > node.parent.upper_bound:
                    node.parent.upper_bound = node.V
                if node.V < node.parent.lower_bound:
                    node.parent.lower_bound = node.V

            self.tree_data[node.get_state()] = (node.visit_count, node.score, node.V)

            node = node.parent

        # temp.print(True)