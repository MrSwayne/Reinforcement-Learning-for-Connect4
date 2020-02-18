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
                normalised_score = (child.V - node.best_child.V) / ((node.best_child.V - node.worst_child.V) + 1)
                score = normalised_score + self.e * math.sqrt(math.log(pvc) / cvc)
                #score = node.V + 2* (self.e * math.sqrt(2 * math.log(pvc) / cvc))
                #print(score, "....", normalised_score, "......", child.V, "-", child.visit_count)
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

    def save_data(self, path):
        super().save_data(path)


def backpropagate(self, node, reward, num_steps):
    reward *= (self.gamma ** (num_steps - 1))

    alpha = 1 / (1 + node.visit_count)
    node.V = node.V + alpha * (reward - node.V)

    while node is not None:

        if reward > 0:
            node.score += 1
        node.visit_count += 1

        if node.parent is not None:
            reward *= -self.gamma
            alpha = 1 / (node.parent.visit_count)
            # node.parent.V = node.parent.V + alpha * (self.reward(node, node.state) + self.gamma * node.V - node.parent.V)
            node.parent.V = node.parent.V + alpha * (reward + self.gamma * node.V - node.parent.V)
            if node.V > node.parent.best_child.V:
                node.parent.best_child = node
            if node.V < node.parent.worst_child.V:
                node.parent.worst_child = node

        if self.learning:
            self.tree_data[node.get_state()] = (node.visit_count, node.score, node.V)
        node = node.parent


    def save_data(self, path):
        print("Saving data now.")

        if not os.path.isdir(self.get_name()):
            os.makedirs(self.get_name())

        if not os.path.isfile(self.get_name() + "/" + path):
            f = open(self.get_name() + "/" + path, "w+")
            f.close()
        with open(self.get_name() + "/" + path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(["state", "state", "turn", "visit count", "score", "value"])
            for state, node in self.tree_data.items():
                writer.writerow([state[0], state[1], state[2], node[0], node[1], node[2]])
        print("Completed writing : ", len(self.tree_data), " rows to ", path)

    def load_data(self, path):
        print("Loading Tree data, ", path)
        self.tree_data = {}

        if not os.path.isdir(self.get_name()):
            os.makedirs(self.get_name())

        if not os.path.isfile(self.get_name() + "/" + path):
            f = open(self.get_name() + "/" + path, "w+")
            f.close()

        with open(self.get_name() + "/" + path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            headers = True
            for row in reader:
                if headers:
                    headers = False
                    continue

                try:
                    self.tree_data[tuple([int(row[0]), int(row[1]), int(row[2])])] = (int(row[3]), float(row[4]), float(row[5]))
                except Exception as e:
                    print(e)
                    print("error loading row: ", row)
        print("Succesfully loaded data, length: ", len(self.tree_data))
