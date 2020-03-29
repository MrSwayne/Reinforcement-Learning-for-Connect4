from Algorithms.Algorithm import *
from Core.IO import IO
from Core import LOGGER

#logger = LOGGER.attach(__name__)
class MCTS(Algorithm):

    def get_values(self):
        list = {}
        if self.root is None:
            return list
        for child in self.root.children:
            list[child.prev_action] = child.V
        return list

    def get_name(self):
        return "MCTS"

    def max_exploration(self, booli):
        logger.info("Setting max exploration to : " + str(booli))
        if booli:
            self.e = 5
        else:
            self.e = self._e


    def __init__(self, memory = None, duration=None, depth=None, n=100, e=0.5, g=0.9, l=1, a = 0.005, debug=False):
        super().__init__()

        self.a = a
        self.e = e
        self._e = e
        self.duration = duration
        self.depth = depth
        self.n = n
        self.end = None
        self.gamma = g
        self.lambd = l
        self.root = None
        self.debug = debug
        self.memory = memory
        self.MAX_REWARD = 1
        self.MIN_REWARD = -1
        self.data = {}


        logger.info("n: " + str(self.n) + " g: " + str(self.gamma) + " e: " + str(self.e) + " mem: " + str(self.memory))
        if memory is not None or memory is not "":
            self.load_memory()

        if not duration and not depth and not n:
            self.n = 250

    def clear_memory(self):
        print("Clearing ", len(self.data))
        self.root = None
        self.data = {}

    def set_memory(self, data):
        print("Overwriting : " + str(len(self.data)) + " with " + str(len(data)))
        logger.info("Overwriting : " + str(len(self.data)) + " with " + str(len(data)))
        self.data = data
        self.root = None

    def get_memory(self):
        return self.data

    def load_memory(self):
        self.data = IO.load(self.memory)

    def save_memory(self, tag = ""):
        IO.write(self.memory + tag, self.data)

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
        if self.learning is False:
            self.root = None

        if self.root is not None:

            if not self.learning:
                self.root.parent = None

            self.expand(self.root)
            children = self.root.children

            self.root = None
            # Select child to be the opponent's move, as opposed to discarding the whole search tree
            for child in children:
                if child.get_state() == state.get_state():
                    self.root = child
                    break



        # If tree has not been initialised previously, or it couldn't find the opponent's move, the tree is discarded
        if self.root is None:
            logger.error("Creating new tree: "+ str(len(self.data)) +  ": " + str(self.learning))
            self.root = Tree.create_tree(state, self.data, self.learning)

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


        logger.debug(str(self.root.player) + " : " + str(self.root.dump()) + " : " + str(best_child.prev_action))
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
        return reward, num_steps

    def expand(self, node):
        node.create_children()

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

    @abstractmethod
    def tree_policy(self, node):
        pass

    @abstractmethod
    def child_policy(self, node):
        pass