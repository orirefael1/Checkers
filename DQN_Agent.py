import torch
import random
import math
from DQN import DQN
from Constant import *
from State import State
from Checkers import Checkers
import numpy as np

class DQN_Agent:
    def __init__(self, player = 1, parametes_path = None, train = True, env= None):
        self.DQN = DQN()
        if parametes_path:
            self.DQN.load_params(parametes_path)
        self.player = player
        self.train = train
        self.setTrainMode()

    def setTrainMode (self):
          if self.train:
              self.DQN.train()
          else:
              self.DQN.eval()

    def get_Action (self, state:State, epoch = 0, events= None, train = True, graphics = None, black_state = None) -> tuple:
        actions = state.legal_actions
        if self.train and train:
            epsilon = self.epsilon_greedy(epoch)
            rnd = random.random()
            if rnd < epsilon:
                return random.choice(actions)
        
        # if self.player == 1:
        state_tensor, action_tensor = state.toTensor()
        # elif not black_state:
        #     black_state = state.reverse()
        #     state_tensor, action_tensor = black_state.toTensor()
        # else:
        #     state_tensor, action_tensor = black_state.toTensor()

        expand_state_tensor = state_tensor.unsqueeze(0).repeat((len(action_tensor),1))
        
        with torch.no_grad():
            Q_values = self.DQN(expand_state_tensor, action_tensor)
        max_index = torch.argmax(Q_values)
        return actions[max_index]

    def get_Actions (self, states_tensor: State, dones) -> torch.tensor:
        actions = []
        boards_tensor = states_tensor[0]
        actions_tensor = states_tensor[1]
        for i, _ in enumerate(boards_tensor):
            if dones[i].item():
                actions.append((0,0, 0,0))
            else:
                state = State.tensorToState(state_tuple=(boards_tensor[i],actions_tensor[i]),player=self.player)
                actions.append(self.get_Action(state, train=False))
        return torch.tensor(actions)
        
    # def get_Actions (self, states_tensor: State, dones) -> torch.tensor:
    #     actions = []
    #     boards_tensor = states_tensor[0]
    #     actions_tensor = states_tensor[1]
    #     for i, board in enumerate(boards_tensor):
    #         if dones[i].item():
    #             actions.append((0,0))
    #         else:
    #             actions.append(self.get_Action(State.tensorToState(state_tuple=(boards_tensor[i],actions_tensor[i]),player=self.player), train=False))
    #     return torch.tensor(actions)

    def epsilon_greedy(self,epoch, start = epsilon_start, final=epsilon_final, decay=epsiln_decay):
        res = final + (start - final) * math.exp(-1 * epoch/decay)
        return res
    
    def loadModel (self, file):
        self.model = torch.load(file)
    
    def save_param (self, path):
        self.DQN.save_params(path)

    def load_params (self, path):
        self.DQN.load_params(path)

    def __call__(self, events= None, state=None):
        return self.get_Action(state)


#################################og###########################################################

# class DQN_Agent:
#     def __init__(self, player = 1, parametes_path = None, train = True, env: Checkers =None ):
#         self.DQN = DQN()
#         if parametes_path:
#             self.DQN.load_params(parametes_path)
#         self.player = player
#         self.train = train
#         self.setTrainMode()
#         self.env = env

#     def setTrainMode (self):
#           if self.train:
#               self.DQN.train()
#           else:
#               self.DQN.eval()
  
#     def get_Action (self, state:State, epoch = 0, events= None, train = True, graphics = None, black_state = None) -> tuple:
#         # if state.blocked == 1:
#         #         return (-1,-1), (-1, -1)
        
#         actions = state.legal_actions
#         # actions_tensor = torch.tensor(actions).reshape(-1,4)
#         if self.train and train:
#             epsilon = self.epsilon_greedy(epoch)
#             rnd = random.random()
#             if rnd < epsilon:
#                 return random.choice(actions)
        
#         if self.player == 1:
#             state_tensor, actions_tensor = state.toTensor()
#         # elif not black_state:
#         #     black_state = state.reverse()
#         #     state_tensor = black_state.toTensor()
#         # else:
#         #     state_tensor = black_state.toTensor()

#         expand_state_tensor = state_tensor.unsqueeze(0).repeat((len(actions_tensor),1))
        
#         with torch.no_grad():
#             Q_values = self.DQN(expand_state_tensor, actions_tensor)
#         max_index = torch.argmax(Q_values)
#         return actions[max_index]

#     def get_Actions (self, states_tensor, dones) -> torch.tensor:
#         actions = []
#         for i, board in enumerate(states_tensor):
#             if dones[i].item():
#                 actions.append(((0,0), (0,0)))
#             else:
#                 state = State.tensorToState(state_tensor=board,player=self.player)
#                 actions.append(self.get_Action(state, train=False))
#         return torch.tensor(actions).reshape(-1, 4)

#     def epsilon_greedy(self,epoch, start = epsilon_start, final=epsilon_final, decay=epsiln_decay):
#         res = final + (start - final) * math.exp(-1 * epoch/decay)
#         return res
    
#     def loadModel (self, file):
#         self.model = torch.load(file)
    
#     def save_param (self, path):
#         self.DQN.save_params(path)

#     def load_params (self, path):
#         self.DQN.load_params(path)

#     def __call__(self, events= None, state=None):
#         return self.get_Action(state)
