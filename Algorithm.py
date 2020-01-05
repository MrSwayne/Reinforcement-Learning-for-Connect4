from abc import abstractmethod
import random
from copy import deepcopy
import math
from datetime import datetime, timedelta

class Algorithm():

    algorithms = ["MINIMAX", "MCTS", "RANDOM"]

    def __init__(self):
        pass

    @abstractmethod
    def get_move(self, state, player):
        pass

class MCTS(Algorithm):

    path = 'state_values.csv'

    def __init__(self,duration = None, depth = None, n = None, e = 1, g = 1.0, a = 0.8, memory=True):
        super().__init__()
        self.e = e
        self.duration = duration
        self.depth = depth
        self.n = n
        self.a = a
        self.end = None
        self.g = g
        self.tree_data = {}
        self.memory = memory
        self.path = "tree_data.csv"
        self.num_new_states = 0
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


    def get_move(self, state, player):

        #Initialise computational starts
        self.end = None
        self.current_n = 0

        #Create game tree
        self.root = self.create_node(parent=None, action=-1, state=state, player=player)

        #Based on initial conditions like time per turn, or X amount of simulations etc.
        while self.should_continue():
            self.current_n += 1

            node = self.select_node()

            if not node.state.game_over and node.visit_count != 0:
                node = self.expand(node)

            winner = self.simulation(node)

            self.backpropagate(node, winner)

        return self.child_policy(self.root).prev_action

    def select_node(self):
        node = self.root

        #Go until leaf node
        while (len(node.children) != 0):
            node = self.tree_policy(node)

        if node.get_state() not in self.tree_data:
            self.tree_data[node.get_state()] = (node.score, node.visit_count)

        return node

    def expand(self, node):
        for action in node.state.get_actions():
            child = self.create_node(parent=node, action=action, player=node.state.get_player_turn())
            node.children.append(child)

        return self.tree_policy(node)


    def simulation(self, node):

        winner = node.state.check_win()

        terminal_state = self.rollout_policy(node.state)

        return terminal_state.check_win()

    def backpropagate(self, node, winner):

        #default MCTS

       # next_value
        while node.parent is not None:
            if node.player == winner:
                node.score += 1
            node.visit_count += 1

            self.tree_data[node.get_state()] = (node.score, node.visit_count)
            node = node.parent

        '''
        #RL
        while node.parent is not None:
            node.visit_count += 1
            node.score += reward
            self.tree_data[node.get_state()] = (node.score, node.visit_count)
            node = node.parent
 
        node.visit_count += 1


        alpha = 1 / node.visit_count
        node.score = node.score + alpha * (reward)
        self.tree_data[node.get_state()] = (node.score, node.visit_count)
        while node.parent is not None:
            node.parent.visit_count += 1

            #Learning Rate inversely proportional to amount of visits of the state, more visits = smaller update step
            alpha = 1 / node.parent.visit_count
            node.parent.score = node.parent.score + alpha * (reward + self.g *node.score - node.parent.score)
            self.tree_data[node.parent.get_state()] = (node.parent.score, node.parent.visit_count)
            if node.parent.upper_bound < node.score:
                node.parent.upper_bound = node.score
            if node.parent.lower_bound > node.score:
                node.parent.lower_bound = node.score
            node = node.parent
    '''

    def reward(self, state):
        check_win = state.check_win()
        if check_win == self.root.player:
            return 1
        elif(int(check_win) <= 0):
            return 0
        else:
            return -1


    #UCB
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
              #  cs = (cs - node.upper_bound) / (node.upper_bound - node.lower_bound) + 1

                score = cs / cvc + (self.e * math.sqrt(math.log(pvc) / cvc))

            if score > max_score:
                best_children = []
                max_score = score
            if score >= max_score:
                best_children.append(child)

        return random.choice(best_children)

    def rollout_policy(self, state):
        temp_state = deepcopy(state)
        while not temp_state.game_over:
            actions = temp_state.get_actions()
            if len(temp_state.get_actions()) > 0:
                temp_state.place(random.choice(actions))
            else:
                break
        return temp_state

    def child_policy(self, node):
        most_visits = float("-inf")
        best_child = None

        for child in node.children:
            if child.visit_count >= most_visits:
                most_visits = child.visit_count
                best_child = child
        return best_child


    def create_node(self, parent=None, action=-1, state=None, player=None):

        if parent is None:
            dummy_node = Node(parent=None, state=None, player=None, prev_action=None, depth=None)
            node = Node(parent=dummy_node, state=state, player=player, prev_action=action, depth=0)
        else:
            temp_board = deepcopy(parent.state)
            temp_board.place(action)
            node = (Node(parent=parent, state=temp_board, player=player, prev_action=action, depth=parent.depth + 1))

        state = node.get_state()

        if state in self.tree_data:
            node.score, node.visit_count = self.tree_data[state]
       #     if state == (0,0):
       #         print("Loading: ", node.score, "->", node.visit_count)

        return node


class Node:
    def __init__(self, parent, state, player, prev_action, depth=0):
        self.children = []
        self.parent = parent
        self.visit_count = 0
        self.score = 0
        self.state = state
        self.player = player
        self.prev_action = prev_action
        self.depth = depth
        self.tag = str(depth) + "_" + str(prev_action)
        self.upper_bound = 1
        self.lower_bound = 0

    def get_state(self):
        board, mask = self.state.get_state(self.player)
        return (board, mask)

    def __repr__(self):
        return "{" + str(self.tag) + "," + str(self.score) + "," + str(self.visit_count)  + "}"

    def print(self):
        print(repr(self), "->", self.children)
        for child in self.children:
            child.print()



class Random(Algorithm):

    def __init__(self):
        super().__init__()

    def get_move(self, state, player):
        choice = random.choice(state.get_actions())

        return choice



class Minimax(Algorithm):

    def __init__(self, max_depth = 4):
        super().__init__()
        self.depth = max_depth

    def get_move(self, state, player):
        self.player = player
        return self.minimax(state)

    def minimax(self, board, depth=0):
        winner = board.check_win()
        if winner == self.player:
            return 1
        elif winner in board.players:
            return -1
        elif int(winner) == 0:
            return 0

        if depth == self.depth:
                return 0

        max_score = float('-inf')

        actions = board.get_actions()

        choices = []
        for action in actions:
            score = float('-inf')
            new_board = deepcopy(board)

            new_board.place(action)
            score -= self.minimax(new_board, depth + 1)

            if score == max_score:
                choices.append(action)

            elif score > max_score:
                max_score = score
                choices.clear()
                choices.append(action)

        if len(choices) > 0 and depth == 0:
            return random.choice(choices)
        return max_score