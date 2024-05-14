import numpy as np
from State import State
from Graphics import *
import torch


class Checkers:
    def __init__(self, state:State = None) -> None:
        if state is None:
            #self.state = self.get_init_state((ROWS, COLS))
            self.state = self.get_init_state()
        else:
            self.state = state
        # self.set_legal_actions(self.state)

    def get_init_state(self):
        # board = np.zeros(Rows_Cols,int)
        board = np.array([[-1, 2, -1, 2, -1, 2, -1, 2],
                          [2, -1, 2, -1, 2, -1, 2, -1],
                          [-1, 2, -1, 2, -1, 2, -1, 2],
                          [0, -1, 0, -1, 0, -1, 0, -1],
                          [-1, 0, -1, 0, -1, 0, -1, 0],
                          [1, -1, 1, -1, 1, -1, 1, -1],
                          [-1, 1, -1, 1, -1, 1, -1, 1],
                          [1, -1, 1, -1, 1, -1, 1, -1]])

        state = State (board, 1)
        self.set_legal_actions(state=state) 
        return state

    def is_free(self, row_col: tuple[int, int], state: State):
        row, col = row_col
        return state.board[row, col] != 0

    def is_inside(self, row_col, state: State):
        row, col = row_col
        board_row, board_col = state.board.shape
        return 0 <= row < board_row and 0 <= col < board_col

    def is_eat(self, start_row_col: tuple[int, int], dir_row_col: tuple[int, int], state: State, to_dir_row = None, to_dir_col = None):       
        start_row, start_col = start_row_col
        dir_row, dir_col = dir_row_col
        if state.board[dir_row_col] != 0:
           return False       
        if start_col < dir_col:
            to_dir_col = 1
        else:
            to_dir_col = -1
        if start_row < dir_row:
            to_dir_row = 1
        else:
            to_dir_row = -1
        row_enemy = start_row + to_dir_row
        col_enemy = start_col + to_dir_col
        if state.board[row_enemy][col_enemy] in [state.get_opponent(), state.get_opponent()+2] and int(abs(dir_row - start_row)) == 2 and int(abs(dir_col - start_col)) == 2:
           return True
        return False

    def eat(self, start_row_col: tuple[int, int], dir_row_col: tuple[int, int], state: State, row_enemy = None, col_enemy = None):
        start_row, start_col = start_row_col
        dir_row, dir_col = dir_row_col
        row_enemy = int(abs(dir_row + start_row)/2)
        col_enemy = int(abs(dir_col + start_col)/2)
        piece = state.board[start_row_col]
        state.board[row_enemy][col_enemy] = 0
        state.board[start_row][start_col] = 0
        state.board[dir_row][dir_col] = piece

    def flip_piece(self, row_col, state: State):
        row, col = row_col
        if state.board[row][col] == 1:
            state.board[row][col] = 2
        else:
            state.board[row][col] = 1  
     
    def move(self, action, state: State):
        if action == ((-1, -1), (-1, -1)):
            state.blocked = 2
            state.switch_player()
            self.set_legal_actions(state)
            return True
        
        if state.blocked == 2:
            state.blocked = 0
            state.after_eat = 1

        start_row_col, dir_row_col = action
        start_row, start_col = start_row_col
        dir_row, dir_col = dir_row_col
        piece = state.board[start_row_col]
        # if self.is_legal_move(start_row_col, dir_row_col, state, state.after_eat):
        if self.is_eat(start_row_col, dir_row_col, state):
            self.eat(start_row_col, dir_row_col, state)             
            if self.can_eat_more(state, dir_row_col):
                state.blocked = 1
                state.blocked_row_col = dir_row_col
            state.after_eat = 0
            self.queen(state, dir_row_col)
            state.switch_player()
            self.set_legal_actions(state)
            return True
        state.board[dir_row][dir_col] = piece
        state.board[start_row][start_col] = 0
        self.queen(state, dir_row_col)
        state.switch_player()
        self.set_legal_actions(state)
        return True

    def is_legal_move(self, start_row_col: tuple[int, int], dir_row_col: tuple[int, int], state: State, after_eat = None):
        start_row, start_col = start_row_col
        dir_row, dir_col = dir_row_col
        if state.blocked == 2 and start_row_col != state.blocked_row_col:
            return False

        if after_eat == 1 and state.board[dir_row][dir_col] == 0:
            if self.is_eat(start_row_col, dir_row_col, state):
                return True
        if state.board[start_row][start_col] in [3, 4] and state.board[dir_row][dir_col] == 0 and after_eat != 1:
            if int(abs(dir_row - start_row)) == 1 and int(abs(dir_col - start_col)) == 1:
                return True
            if self.is_eat(start_row_col, dir_row_col, state):
                return True
        if state.board[dir_row][dir_col] == 0 and self.is_not_reverse(start_row_col, dir_row_col, state) and after_eat != 1:
            if int(abs(dir_row - start_row)) == 1 and int(abs(dir_col - start_col)) == 1:
                return True
            if self.is_eat(start_row_col, dir_row_col, state):
                return True
        
        return False

    def is_not_reverse (self, start_row_col, dir_row_col, state: State):
        start_row, start_col = start_row_col
        dir_row, dir_col = dir_row_col
        if state.player in [1, 3] and dir_row < start_row:
            return True
        if state.player in [2, 4] and dir_row > start_row:
            return True
        return False
   
    def get_legal_actions(self, state: State):   # to do
        return state.legal_actions

    def set_legal_actions (self, state):
        
        if state.blocked == 1:
            state.legal_actions = [((-1,-1), (-1, -1))]
            return

        if state.player == 1:
            my_pieces = np.where(state.board == 1)
            my_pieces = list(zip(my_pieces[0], my_pieces[1]))
            my_queens = np.where(state.board == 3)
            my_queens = list(zip(my_queens[0], my_queens[1]))
        else:
            my_pieces = np.where(state.board == 2)
            my_pieces = list(zip(my_pieces[0], my_pieces[1]))
            my_queens = np.where(state.board == 4)
            my_queens = list(zip(my_queens[0], my_queens[1]))

        empties = np.where(state.board == 0)
        empties = list(zip(empties[0], empties[1]))

        legal_actions = []
        if state.blocked == 2:
            for empty in empties:
                if self.is_eat(state.blocked_row_col, empty, state, state.after_eat):
                    legal_actions.append((state.blocked_row_col, empty))
            state.legal_actions = legal_actions    
            return 
        
        for piece in my_pieces:
            for empty in empties:
                if self.is_legal_move(piece, empty, state, state.after_eat):
                    legal_actions.append((piece, empty))
        for queen in my_queens:
            for empty in empties:
                if self.is_legal_move(queen, empty, state, state.after_eat):
                    legal_actions.append((queen, empty))
        state.legal_actions = legal_actions

    def is_end_of_game(self, state: State):
        legal_moves = self.get_legal_actions(state)
        if legal_moves:
            return False
        return True

    def get_next_state(self, action, state):
        next_state = state.copy()
        self.move(action, next_state)
        # next_state/legal_action = self.get_legal_action
        return next_state
    
    def legal_Choose (self, action, state: State):
        if state.blocked == 2 and action != state.blocked_row_col:
            return False
        return state.board[action] == state.player or state.board[action] == state.player+2

    def can_eat_more (self, state, row_col):
        row, col = row_col
        count = 0
        directions = [(2,2), (2,-2), (-2,2), (-2,-2)]
        for dir in directions:          
            dir_row, dir_col = dir  
            new_row, new_col = row + dir_row, col + dir_col
            new_row_col = new_row, new_col
            if new_row < 0 or new_col < 0 or new_row > 7 or new_col > 7:
                continue
            if self.is_eat(row_col, new_row_col, state):
                count += 1
        if count > 0 :
            return True
        return False
    
    def get_all_next_states (self, state: State) -> tuple:
        legal_actions = self.get_legal_actions(state)
        next_states = []
        for action in legal_actions:
            next_states.append(self.get_next_state(action, state))
        return next_states, legal_actions
    
    def in_bound(self, row, col):
        if row < 0 or col < 0 or row > 7 or col > 7:
                return False
        return True
    
    def toTensor (self, list_states, device = torch.device('cpu')) -> tuple:
        list_board_tensors = []
        list_legal_actions = []
        for state in list_states:
            board_tensor, legal_actions = state.toTensor(device) 
            list_board_tensors.append(board_tensor)
            list_legal_actions.append(torch.tensor(legal_actions))
        return torch.vstack(list_board_tensors), torch.vstack(list_legal_actions)
    
    def reward (self, state : State, action = None) -> tuple:
                
        if (self.is_end_of_game(state)):
            player1, player2 = state.score()
            if player1 > player2:
                return 10, True
            if player2 > player1:
                return -10, True
            return 0, True
        
        start, dir = action
        if abs(start[0]-dir[0]) == 2:
            if state.player == 2:  # after move and switch player
                return 0.5, False
            else:
                return -0.5, False
        return 0, False


######################## Queen ####################################

    def queen(self, state: State, row_col):
        row, col = row_col
        if state.player == 1 and row == 0:
            state.board[row][col] = 3
        if state.player == 2 and row == 7:
            state.board[row][col] = 4

    def is_move_queen(self, start_row_col: tuple[int, int], dir_row_col: tuple[int, int], state: State):
        start_row, start_col = start_row_col
        dir_row, dir_col = dir_row_col

        
        if state.board[dir_row][dir_col] != 0:
            return "Ocuppied"
        if abs(dir_row-start_row) != abs(dir_col-start_col): # check if diagonal
            return "No diagonal"
        
        if start_col < dir_col:
            to_dir_col = 1
        else:
            to_dir_col = -1
        if start_row < dir_col:
            to_dir_row = 1
        else:
            to_dir_row = -1

        diagonal_length = abs(dir_row-start_row)
        diagonal = np.zeros(diagonal_length)
        row = start_row + to_dir_row
        col = start_col + to_dir_col

        for i in range(diagonal_length):
            diagonal[i] = state.board[row,col]
            row = start_row + to_dir_row
            col = start_col + to_dir_col

        empties = np.count_nonzero(diagonal==0)
        opponents = np.count_nonzero(diagonal == state.get_opponent())
        players = np.count_nonzero(diagonal == state.player)

        if empties == diagonal_length:
            return "Move"
        
        if players > 0:
            return "illegal"
        
        if opponents == 1:
            index = np.where(diagonal==state.get_opponent())
            return start_row + index[0]*to_dir_row, start_col + index[1]*to_dir_col
        
        return "illegal"
    

    

    def is_eat_queen(self):
        pass

    def eat_queen (self):
        pass

    def get_legal_action_queen(self):
        pass
