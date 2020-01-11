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
    def get_move(self, state):
        pass

class MCTS(Algorithm):

    path = 'state_values.csv'

    def __init__(self,duration = None, depth = None, n = None, e = 1, g = 0.9, l = 1 , memory=True):
        super().__init__()
        self.e = e
        self.duration = duration
        self.depth = depth
        self.n = n
        self.end = None
        self.gamma = g
        self.lambd = l
        self.tree_data = {}
        self.memory = memory
        self.path = "tree_data.csv"
        self.num_new_states = 0
        self.root = None

        self.MAX_REWARD = 1
        self.MIN_REWARD = 0

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

        #Initialise computational starts
        self.end = None
        self.current_n = 0

        #Create game tree

        if self.root is not None:
            children = self.root.children
            self.root = None
            for child in children:
                if child.get_state() == state.get_state(child.player):
                    self.root = child
                    break

        if self.root is None:
            self.root = self.create_node(parent=None, action=-1, state=state, player=state.get_player_turn())

        #Based on initial conditions like time per turn, or X amount of simulations etc.
        while self.should_continue():
            self.current_n += 1

            node = self.select_node()

            if not node.state.game_over and node.visit_count != 0:
                node = self.expand(node)

            reward, num_steps = self.simulation(node)

            self.backpropagate(node, reward, num_steps)

        best_child = self.child_policy(self.root)
    #    print(self.root.children, "\t", best_child.prev_action, "\t")
        self.root = best_child

        return best_child.prev_action

    def select_node(self):
        node = self.root

        #Go until leaf node
        while (len(node.children) != 0):
            node = self.tree_policy(node)

        if node.get_state() not in self.tree_data:
            self.tree_data[node.get_state()] = (node.visit_count, node.V)

        return node

    def expand(self, node):
        for action in node.state.get_actions():
            child = self.create_node(parent=node, state=node.state, action=action)
            node.children.append(child)

        return self.tree_policy(node)


    def simulation(self, node):

        terminal_state, num_steps = self.rollout_policy(node.state)
        reward = self.reward(node, terminal_state)

        if num_steps == -1:
            node.print(True)
            print(node.player)
            node.state.print()
            terminal_state.print()
            print(terminal_state.winner)
            print(reward)
        return reward, num_steps

    def backpropagate(self, node, reward, num_steps):

        #default
        child_map = {}

      #  print("Backpropagating ", node.player, " : ", reward)
     #   node.print(backwards=True)
        temp = node
        player = node.player

        td_error = (self.gamma ** (num_steps - 1)) * reward - node.V
        eligibility_trace = 1
        temp = node

        while node is not None:
            td_error *= -1
            node.visit_count += 1

            alpha = 1 / node.visit_count
            node.V = node.V + alpha * eligibility_trace * td_error
            eligibility_trace = eligibility_trace * self.gamma * self.lambd

            self.tree_data[node.get_state()] = (node.visit_count, node.V)

            node = node.parent


        '''
        while node.parent is not None:
            node.visit_count += 1
            alpha = 1 / (1 + node.visit_count)
            node.V = node.V + alpha * (reward - node.V)
            reward *= -1
            node = node.parent

            if child_map[node.player] is None:
                child_map[node.player] = node
                child = node
    #    temp = node
                reward = 0
            else:
                child = child_map[node.player]
                reward = self.reward(child, child.state)




            child = child_map[node.player]
            reward = self.reward(child, child.state)

            alpha = 1 / (1 + node.visit_count)
       #     print("OLD:", node.V, "<-", node.player)

            discount_factor = self.g ** (num_steps)
            node.V = node.V + alpha * (reward + ((discount_factor * child.V) - node.V))
            num_steps += 1
       #     print("NEW:", node.V)

            self.tree_data[node.get_state()] = (node.visit_count, node.V)
            child_map[node.player] = node
            node = node.parent
        
       # print()
       
    '''
       # temp.print(True)

    def reward(self,node, state):
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
               # cs = (node.V - node.upper_bound) / (node.upper_bound - node.lower_bound) + 1

                score = child.V + 2 * (self.e * math.sqrt(2 * math.log(pvc) / cvc))

            if score > max_score:
                best_children = []
                max_score = score
            if score >= max_score:
                best_children.append(child)

        return random.choice(best_children)

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

    def child_policy(self, node):
        highest_val = float("-inf")
        best_child = None

        for child in node.children:
            if child.V >= highest_val:
                highest_val = child.V
                best_child = child
        return best_child

    def create_dummy_node(self, parent=None):
        return Node(parent=parent, state=None, player=None, prev_action=None, depth=-1)

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
            node.visit_count, node.V = self.tree_data[_state]


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
        self.V = 0.5

    def get_state(self):
        return self.state.get_state()

    def __repr__(self):
        return "{" + str(self.depth) + "__" + str(self.prev_action) + ","  + (str(round(self.V, 4))) + "," + str(self.visit_count)+ "," +  str(self.player) + "}"

    def print(self, backwards=False):

        if backwards:
            temp_node = self
            list = []
            while(temp_node is not None):
                list.append(temp_node)
                temp_node = temp_node.parent

            print(list)
        else:
            print(repr(self), "->", self.children)
            for child in self.children:
                child.print()



class Random(Algorithm):

    def __init__(self):
        super().__init__()

    def get_move(self, state):
        choice = random.choice(state.get_actions())

        return choice



class Minimax(Algorithm):

    def __init__(self, max_depth = 4):
        super().__init__()
        self.depth = max_depth

    def get_move(self, state):
        self.player = state.get_player_turn()
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