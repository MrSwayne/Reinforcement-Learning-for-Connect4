from Algorithms.MCTS import *

class MCTS_UCT(MCTS):

    def __init__(self, duration=None, depth=None, n=2000, e=1.414, g=0.9, l=1, debug=False):
        super().__init__(duration, depth, n, e, g, l, debug)

        self.MAX_REWARD = 1
        self.MIN_REWARD = 0

    def create_node(self, parent=None, action=-1, state=None, player=None):

        if parent is None:
            node = Node(parent=None, state=state, player=player, prev_action=action, depth=0)
        else:
            temp_board = deepcopy(parent.state)
            temp_board.place(action)
            node = (Node(parent=parent, state=temp_board, player=temp_board.get_player_turn(), prev_action=action, depth=parent.depth + 1))

        _state = node.get_state()

        if _state in self.tree_data:
            node.visit_count, node.score, node.V = self.tree_data[_state]

        return node


    def get_name(self):
        return "MCTS_UCT"

    def reward(self, node, state):
        if not state.game_over:
            check_win = state.check_win()
        else:
            check_win = state.winner

        if(int(check_win) == int(node.player)):
            return self.MAX_REWARD
        elif(int(check_win) < 0):
            return 0
        elif(int(check_win) == 0):
            return 0
        else:
            return self.MIN_REWARD

    def select_node(self):
        node = super().select_node()

        if node.get_state() not in self.tree_data:
            self.tree_data[node.get_state()] = (node.visit_count, node.score)

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
            if node.player != player:
                node.score += reward

            node.visit_count += 1

            self.tree_data[node.get_state()] = (node.visit_count, node.score)

            node = node.parent
