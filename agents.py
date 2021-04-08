import random
import math

BOT_NAME = "connect383bot"

class RandomAgent:
    """Agent that picks a random available move.  You should be able to beat it."""
    def __init__(self, sd=None):
        if sd is None:
            self.st = None
        else:
            random.seed(sd)
            self.st = random.getstate()

    def get_move(self, state):
        if self.st is not None:
            random.setstate(self.st)
        return random.choice(state.successors())


class HumanAgent:
    """Prompts user to supply a valid move."""
    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        prompt = "Kindly enter your move {}: ".format(sorted(move__state.keys()))
        move = None
        while move not in move__state:
            try:
                move = int(input(prompt))
            except ValueError:
                continue
        return move, move__state[move]


class MinimaxAgent:
    """Artificially intelligent agent that uses minimax to optimally select the best move."""

    def get_move(self, state):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None

        for move, state in state.successors():
            util = self.minimax(state)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def min_value(self, state):
        #Base case
        if state.is_full():
            return state.utility()
        #List to hold utility value of each child
        utilities = []
        value = math.inf;
        for moves, child in state.successors():
            utilities.append(self.max_value(child))
            #Take minimum value of best move of opponent
            value = min(utilities)
        return value

    def max_value(self, state):
        #Base case
        if state.is_full():
            return state.utility()
        #List to hold utility value of each child
        utilities = []
        value = -math.inf
        for moves, child in state.successors():
            utilities.append(self.min_value(child))
            #Take maximum value of best move of opponent
            value = max(utilities)

        return value

    def minimax(self, state):
        """Determine the minimax utility value of the given state.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact minimax utility value of the state
        """
        #Max player
        if state.next_player() == 1:
            return self.max_value(state)
        #Min player
        elif state.next_player() == -1:
            return self.min_value(state)
        

        


class MinimaxHeuristicAgent(MinimaxAgent):
    """Artificially intelligent agent that uses depth-limited minimax to select the best move."""

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def min_value(self, state, depth):
        if state.is_full():
            return state.utility()
        elif depth == 0:
            return self.evaluation(state)
        utilities = []
        value = -math.inf
        for moves, child in state.successors():
            utilities.append(self.max_value(child, depth - 1))
            value = min(utilities)
        return value       

    def max_value(self, state, depth):
        if state.is_full():
            return state.utility()
        elif depth == 0:
            return self.evaluation(state)

        utilities = []
        value = -math.inf
        for moves, child in state.successors():
            utilities.append(self.min_value(child, depth - 1))
            value = max(utilities)
        return value

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state.

        The depth data member (set in the constructor) determines the maximum depth of the game 
        tree that gets explored before estimating the state utilities using the evaluation() 
        function.  If depth is 0, no traversal is performed, and minimax returns the results of 
        a call to evaluation().  If depth is None, the entire game tree is traversed.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        #Max player
        if state.next_player() == 1:
            return self.max_value(state, self.depth_limit)
        #Min player
        elif state.next_player() == -1:
            return self.min_value(state, self.depth_limit)

    def unblocked_streaks(self, lst):  
        """Get the lengths of all unblocked streaks of the same element in a sequence."""
        rets = []  # list of (element, length) tuples
        prev = lst[0]
        curr_len = 1
        for curr in lst[1:]:
            if curr == prev:
                curr_len += 1
            else:
                #Modified streaks() method in connect383.py: Return streaks only if next element is open
                if curr == 0:
                    rets.append((prev, curr_len))
                    prev = curr
                    curr_len = 1
        rets.append((prev, curr_len))
        return rets    

    def evaluation(self, state):
        """Estimate the utility value of the game state based on features.

        N.B.: This method must run in O(1) time!

        Args:
            state: a connect383.GameState object representing the current board

        Returns: a heusristic estimate of the utility value of the state
        """

        #Feature: Threats
        s1_score = 0
        s2_score = 0

        #Very similar to calculating score, except it accounts only for open streaks of 2 or higher
        for run in state.get_cols() + state.get_rows() + state.get_diags():
            for elt, length in self.unblocked_streaks(run):
                if elt == 1 and length >= 2:
                    s1_score += length**2
                if elt == -1 and length >= 2:
                    s2_score += length**2
        
        s_score = s1_score - s2_score

        ###Feature: Center moves (Pieces closer to the center columns will have higher score, pieces near center of board will have even more points)
        c1_scores = 0
        c2_scores = 0

        r1_scores = 0
        r2_scores = 0
        #If board has odd number of columns
        if len(state.get_cols()) % 2 != 0:
            center = math.ceil(len(state.get_cols()) / 2) - 1
            center_col = state.get_cols()[center]
            for cell in center_col:
                if cell == 1:
                    c1_scores += 3
                if cell == -1:
                    c2_scores += 3
            for cell in state.get_cols()[center + 1] and state.get_cols()[center - 1]:
                if cell == 1:
                    c1_scores += 2
                if cell == -1:
                    c2_scores += 2             
        #If board has even number of column (2 center spots)
        elif len(state.get_cols()) % 2 == 0:
            l_center = len(state.get_cols())/2 - 1
            r_center = len(state.get_cols())/2

            lcenter_col = state.get_cols()[int(l_center)]
            rcenter_col = state.get_cols()[int(r_center)]

            for cell in lcenter_col and rcenter_col:
                if cell == 1:
                    c1_scores += 3
                if cell == -1:
                    c2_scores += 3
            for cell in state.get_cols()[int(r_center) + 1] and state.get_cols()[int(l_center) - 1]:
                if cell == 1:
                    c1_scores += 2
                if cell == -1:
                    c2_scores += 2               
        
        c_score = c1_scores - c2_scores

        #If board has odd number of rows
        if len(state.get_rows()) % 2 != 0:
            center = math.ceil(len(state.get_rows()) / 2) - 1
            center_row = state.get_rows()[center]
            for cell in center_row:
                if cell == 1:
                    r1_scores += 3
                if cell == -1:
                    r2_scores += 3
            for cell in state.get_rows()[center + 1] and state.get_rows()[center - 1]:
                if cell == 1:
                    r1_scores += 2
                if cell == -1:
                    r2_scores += 2             
        #If board has even number of rows (2 center spots)
        elif len(state.get_rows()) % 2 == 0:
            l_center = len(state.get_rows())/2 - 1
            r_center = len(state.get_rows())/2

            lcenter_row = state.get_rows()[int(l_center)]
            rcenter_row = state.get_rows()[int(r_center)]

            for cell in lcenter_row and rcenter_row:
                if cell == 1:
                    r1_scores += 3
                if cell == -1:
                    r2_scores += 3
            for cell in state.get_rows()[int(r_center) + 1] and state.get_rows()[int(l_center) - 1]:
                if cell == 1:
                    r1_scores += 2
                if cell == -1:
                    r2_scores += 2 

        r_score = r1_scores - r2_scores
               
        
        weighted_total = c_score + 6*r_score + s_score
        return weighted_total
        
        





class MinimaxHeuristicPruneAgent(MinimaxHeuristicAgent):
    """Smarter computer agent that uses minimax with alpha-beta pruning to select the best move."""
    
    def min_value(self, state, a, b, depth):
        if state.is_full():
            return state.utility()
        elif depth == 0:
            return self.evaluation(state)
        utilities = []
        value = math.inf
        for moves, child in state.successors():
            utilities.append(self.max_value(child, a, b, depth - 1))
            value = min(utilities)
            if value <= a: return value
            b = min(b, value)
        return value       

    def max_value(self, state, a, b, depth):
        if state.is_full():
            return state.utility()
        elif depth == 0:
            return self.evaluation(state)
        utilities = []
        value = -math.inf
        for moves, child in state.successors():
            utilities.append(self.min_value(child, a, b, depth - 1))
            value = max(utilities)
            if value >= b: return value;
            a = max(a, value)
        return value


    def minimax(self, state):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        The value should be equal to the one determined by MinimaxAgent.minimax(), but the 
        algorithm should do less work.  You can check this by inspecting the value of the class 
        variable GameState.state_count, which keeps track of how many GameState objects have been 
        created over time.  This agent should also respect the depth limit like HeuristicAgent.

        N.B.: When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  That is, you cannot prune
        the state reached by moving to column 4 before you've explored the state reached by a move
        to to column 1.

        Args: 
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """

        if state.next_player() == 1:
            return self.max_value(state, -math.inf, math.inf, self.depth_limit)
        elif state.next_player() == -1:
            return self.min_value(state, -math.inf, math.inf, self.depth_limit)

        


