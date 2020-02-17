from Algorithms.MCTS_TDUCT import *

class MCTS_TDUCT3(MCTS_TDUCT):

    def get_name(self):
        return "MCTS_TDUCT2"

    def select_node(self):
        node = super().select_node()

        if node.get_state() not in self.tree_data and self.learning:
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

        reward *= (self.gamma ** (num_steps - 1))

        alpha = 1 / (1+node.visit_count)
        node.V = node.V + alpha * (reward - node.V)

        while node is not None:
            node.visit_count += 1

            if node.parent is not None:
                reward *= -self.gamma
                alpha = 1/ (node.parent.visit_count)
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
