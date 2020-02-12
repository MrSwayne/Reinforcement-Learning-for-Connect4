from Algorithms.Algorithm import *
import os
import csv



class MCTS(Algorithm):

    def save_data(self, path):
        print("Saving data now.")

        if not os.path.isdir(self.get_name()):
            os.makedirs(self.get_name())

        if not os.path.isfile(self.get_name() + "/" + path):
            f = open(self.get_name() + "/" + path, "w+")
            f.close()
        with open(self.get_name() + "/" + path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(["state", "state", "turn", "visit count", "score"])
            for state, node in self.tree_data.items():
                writer.writerow([state[0], state[1], state[2], node[0], node[1], node[2] ])
        print("Completed writing : ", len(self.tree_data), " rows")

    def load_data(self, path):
        print("Loading Tree data")
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


    def get_name(self):
        return "MCTS"

    def __init__(self, duration=None, depth=None, n=2000, e=1, g=0.9, l=1, debug=False):
        super().__init__()
        self.e = e
        self.duration = duration
        self.depth = depth
        self.n = n
        self.end = None
        self.gamma = g
        self.lambd = l
        self.tree_data = {}
        self.path = "tree_data.csv"
        self.num_new_states = 0
        self.root = None
        self.debug = debug

        self.MAX_REWARD = 1
        self.MIN_REWARD = -1

        if not duration and not depth and not n:
            self.n = 250

    def should_continue(self):
        if self.duration:
            if not self.end:
                self.end = datetime.now() + self.duration
                return True
            else:
                return datetime.now() < self.end

        if self.n:
            return self.current_n < self.n

        return False

    def get_move(self, state):

        # Initialise computational starts
        self.end = None
        self.current_n = 0

        # Create game tree

        # If the tree has already been created
        if self.root is not None:
            children = self.root.children
            self.root = None

            # Select child to be the opponent's move, as opposed to discarding the whole search tree
            for child in children:
                if child.get_state() == state.get_state(child.player):
                    self.root = child
                    break

        # If tree has not been initialised previously, or it couldn't find the opponent's move, the tree is discarded
        if self.root is None:
            self.root = self.create_node(parent=None, action=-1, state=state, player=state.get_player_turn())

        # Based on initial conditions like time per turn, or X amount of simulations etc.
        while self.should_continue():
            self.current_n += 1

            # Selection
            node = self.select_node()

            # Expansion
            if not node.state.game_over:
                self.expand(node)

            # Simulation
            reward, num_steps = self.simulation(node)

            # Backpropagation
            self.backpropagate(node, reward, num_steps)

        best_child = self.child_policy(self.root)

        if self.debug:
            print(self.root, "->", self.root.children, "\t", best_child.prev_action, "\t")
        self.root = best_child

        return best_child.prev_action

    def select_node(self):
        node = self.root

        # Go until leaf node
        while (len(node.children) != 0):
            node = self.tree_policy(node)

        return node

    def simulation(self, node):
        terminal_state, num_steps = self.rollout_policy(node.state)
        reward = self.reward(node, terminal_state)

        if num_steps < -3 and reward > 0:
            node.state.print()
            print(reward, num_steps)
            terminal_state.print()
        return reward, num_steps

    def expand(self, node):
        for action in node.state.get_actions():
            child = self.create_node(parent=node, state=node.state, action=action)

            if child.V > node.upper_bound:
                node.upper_bound = child.V
            if child.V < node.lower_bound:
                node.lower_bound = child.V

            node.children.append(child)

    def rollout_policy(self, state):
        temp_state = deepcopy(state)

        count = 0
        while not temp_state.game_over:
            actions = temp_state.get_actions()
            if len(temp_state.get_actions()) > 0:
                temp_state.place(random.choice(actions))
                count += 1
            else:
                break
        return temp_state, count


    @abstractmethod
    def backpropagate(self, node, reward, num_steps):
        pass

    @abstractmethod
    def reward(self, node, state):
        pass

        # UCB

    @abstractmethod
    def tree_policy(self, node):
        pass


    @abstractmethod
    def child_policy(self, node):
        pass

    @abstractmethod
    def create_node(self, parent=None, action=-1, state=None, player=None):
        pass

    @abstractmethod
    def save_data(self, path):
        pass

    @abstractmethod
    def load_data(self, path):
        pass