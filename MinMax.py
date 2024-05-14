import pygame
from Graphics import *
from State import State
from Checkers import Checkers

MAXSCORE = 1000

class MinMax:
    
        def __init__(self, player, depth = 2, env : Checkers = None) -> None:
            self.player = player
            if self.player == 1:
                self.opponent = 2
            else:
                self.opponent = 1
            self.depth = depth
            self.environment = env

        def evaluate(self, state:State):
            if self.player == 1:
                opponent = 2
            else:
                opponent = 1 
                 
            board = state.board
            board_array = np.array(board)
            player_pieces_score = np.sum(board_array == self.player)
            player_queen_score = np.sum(board_array == self.player + 2) * 1.5
            opponent_pieces_score = np.sum(board_array == opponent)
            opponent_queen_score = np.sum(board_array == opponent + 2) * 1.5

            return player_pieces_score + player_queen_score - (opponent_pieces_score + opponent_queen_score)
        
        def get_Action(self, events, graphics, state: State):
            # if state.blocked == 1:
            #     return (-1,-1), (-1, -1)

            value, bestAction = self.minMax(state)
            return bestAction

        def minMax(self, state:State):
            visited = set()
            depth = 0
            return self.max_value(state, visited, depth)
            
        def max_value (self, state:State, visited:set, depth):
            
            value = -MAXSCORE

            # stop state
            if depth == self.depth or self.environment.is_end_of_game(state):
                value = self.evaluate(state)
                return value, None
            
            # start recursion
            bestAction = None
            legal_actions = self.environment.get_legal_actions(state)
            for action in legal_actions:
                newState = self.environment.get_next_state(action, state)
                if newState not in visited:
                    visited.add(newState)
                    newValue, newAction = self.min_value(newState, visited,  depth + 1)
                    if newValue > value:
                        value = newValue
                        bestAction = action

            return value, bestAction 

        def min_value (self, state:State, visited:set, depth):
            
            value = MAXSCORE

            # stop state
            if depth == self.depth or self.environment.is_end_of_game(state):
                value = self.evaluate(state)
                return value, None
            
            # start recursion
            bestAction = None
            legal_actions = self.environment.get_legal_actions(state)
            for action in legal_actions:
                newState = self.environment.get_next_state(action, state)
                if newState not in visited:
                    visited.add(newState)
                    newValue, newAction = self.max_value(newState, visited,  depth + 1)
                    if newValue < value:
                        value = newValue
                        bestAction = action

            return value, bestAction 
        

        def max_value_alpha(self, state: State, visited: set, depth, alpha, beta):

            value = float('-inf')

            # stop state
            if depth == self.depth or self.environment.is_end_of_game(state):
                value = self.evaluate(state)
                return value, None

            # start recursion
            bestAction = None
            legal_actions = self.environment.get_legal_actions(state)
            for action in legal_actions:
                newState = self.environment.get_next_state(action, state)
                if newState not in visited:
                    visited.add(newState)
                    newValue, newAction = self.min_value(newState, visited, depth + 1, alpha, beta)
                    if newValue > value:
                        value = newValue
                        bestAction = action

                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break  # Beta cutoff

            return value, bestAction

        def min_value_beta(self, state: State, visited: set, depth, alpha, beta):

            value = float('inf')

            # stop state
            if depth == self.depth or self.environment.is_end_of_game(state):
                value = self.evaluate(state)
                return value, None

            # start recursion
            bestAction = None
            legal_actions = self.environment.get_legal_actions(state)
            for action in legal_actions:
                newState = self.environment.get_next_state(action, state)
                if newState not in visited:
                    visited.add(newState)
                    newValue, newAction = self.max_value(newState, visited, depth + 1, alpha, beta)
                    if newValue < value:
                        value = newValue
                        bestAction = action

                    beta = min(beta, value)
                    if alpha >= beta:
                        break  # Alpha cutoff

            return value, bestAction