from collections import deque
import random
import torch
import numpy as np
from State import State

capacity = 100000
end_priority = 2

class ReplayBuffer:
    def __init__(self, capacity= capacity, path = None) -> None:
        if path:
            self.buffer = torch.load(path).buffer
        else:
            self.buffer = deque(maxlen=capacity)

    def push (self, state : State, action, reward, next_state: State, done):
        action_np = np.array(action).reshape(-1, 4)
        self.buffer.append((state.toTensor(), torch.from_numpy(action_np), torch.tensor(reward), next_state.toTensor(), torch.tensor(done)))
        # if done:
        #     for i in range(end_priority):        
        #         self.buffer.append((state.toTensor(), torch.from_numpy(np.array(action)), torch.tensor(reward), next_state.toTensor(), torch.tensor(done)))
    
    def sample (self, batch_size):
        if (batch_size > self.__len__()):
            batch_size = self.__len__()
        state_tensors, action_tensor, reward_tensors, next_state_tensors, dones = zip(*random.sample(self.buffer, batch_size))
        state_boards, state_actions = zip(*state_tensors)
        states = torch.vstack(state_boards), state_actions
        actions= torch.vstack(action_tensor)
        rewards = torch.vstack(reward_tensors)
        next_board, next_actions = zip(*next_state_tensors)
        next_states = torch.vstack(next_board), next_actions
        done_tensor = torch.tensor(dones).long().reshape(-1,1)
        return states, actions, rewards, next_states, done_tensor

    def __len__(self):
        return len(self.buffer)