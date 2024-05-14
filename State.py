import numpy as np
import torch
from copy import deepcopy

class State:
    def __init__(self, board= None, player = 1, legal_actions = None) -> None:
        self.board = board
        self.player = player
        self.action = None
        self.blocked = 0        # 0 - no block; 1 - blocked; 2 - eat another
        self.blocked_row_col = None
        self.after_eat = 0      # 1 after eat
        self.legal_actions = legal_actions
        

    def get_opponent (self):
        if self.player == 1:
            return 2
        else:
            return 1

    def switch_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def score (self, player = 1) -> tuple[int, int]:
        if player == 1:
            opponent = 2
        else:
            opponent = 1

        player_score = np.count_nonzero((self.board == player) | (self.board == player + 2))
        opponent_score = np.count_nonzero((self.board == opponent) | (self.board == opponent + 2))
        return player_score, opponent_score

    def __eq__(self, other) ->bool:
        b1 = np.equal(self.board, other.board).all()
        b2 = self.player == other.player
        return np.equal(self.board, other.board).all() and self.player == other.player

    def __hash__(self) -> int:
        return hash(repr(self.board) + repr(self.player))
    
    def copy (self):
        newBoard = np.copy(self.board)
        new_state = State(board=newBoard, player=self.player)
        new_state.after_eat = self.after_eat
        new_state.blocked_row_col = self.blocked_row_col
        new_state.blocked = self.blocked
        new_state.action = self.action
        new_state.legal_actions = deepcopy(self.legal_actions)
        return new_state


    def toTensor (self, device = torch.device('cpu')) -> tuple:
        board_np = self.board.reshape(-1)
        board_tensor = torch.tensor(board_np, dtype=torch.float32, device=device)
        actions_np = np.array(self.legal_actions).reshape(-1,4)
        actions_tensor = torch.tensor(actions_np, dtype=torch.int64)
        return board_tensor, actions_tensor
    
    [staticmethod]
    def tensorToState (state_tuple, player):
        board_tensor = state_tuple[0]
        board = board_tensor.reshape([8,8]).cpu().numpy()
        legal_actions_tensor = state_tuple[1]
        legal_actions = legal_actions_tensor.cpu().numpy()
        legal_actions = list(map(tuple, legal_actions))
        return State(board, player=player, legal_actions=legal_actions)
    # def tensorToState (state_tensor, actions_tensor, player):
        
    #     board = board_tensor.reshape([8,8]).cpu().numpy()
    #     state = State(board, player=player)
        
    #     actions_np = actions_tensor.numpy().reshape(-1,2,2)
    #     state.legal_actions = list(map(tuple, map(lambda x: map(tuple, x), actions_np)))
    #     return state

    def reverse (self):
        reversed = self.copy()
        reversed.board = reversed.board * -1
        reversed.player = reversed.player * -1
        return reversed
    
    # def get_legal_actions(self):
    #     return self.legal_actions