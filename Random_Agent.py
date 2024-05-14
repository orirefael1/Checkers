from State import State
from Checkers import Checkers
import random


class Random_Agent:

    def __init__(self, player, env : Checkers) -> None:
        self.player = player
        self.env = env

    def get_Action (self, events= None, graphics = None, state : State = None):
        # if state.blocked == 1:
        #     # state.after_eat = 1
        #     return (-1,-1), (-1, -1)

        # if state.blocked == 2:
        #     legal_actions = self.env.get_legal_actions(state)
        #     # state.blocked = 0
        #     # state.after_eat = 1
        #     return random.choice(legal_actions)

        legal_actions = self.env.get_legal_actions(state)
        return random.choice(legal_actions)
                       

            
    
