import pygame
from Graphics import *
from State import State
from Checkers import Checkers

class Human_Agent:

    def __init__(self, player, env : Checkers) -> None:
        self.player = player
        self.mode = 1
        self.start = None
        self.env = env

    def get_Action (self, events= None, graphics: Graphics = None, state : State = None):
        
        if state.blocked == 1:
            return (-1,-1), (-1, -1)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row_col = graphics.calc_row_col(pos) 
                print (row_col)
                if state.blocked == 2:
                    if self.env.is_legal_move(state.blocked_row_col, row_col, state, 1):
                        # state.blocked = 0
                        # state.after_eat = 1
                        return state.blocked_row_col, row_col
                if self.mode == 1:
                    if self.env.legal_Choose(state = state, action = row_col):
                        self.start = row_col
                        print("legal choise", self.start)
                        self.mode = 2
                    else:
                        #blink
                        print("illegal")
                    return None
                else: # mode = 2
                    if self.env.is_legal_move (self.start, row_col, state):
                        self.mode = 1
                        return (self.start), (row_col)
                    else:
                        self.mode = 1
                       
        return None
            
    
