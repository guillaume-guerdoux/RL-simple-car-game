import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

import torch.optim as optim
from torch.autograd import Variable


class Agent(nn.Module):
    """Basic NN agent"""
    def __init__(self):
        super(Agent, self).__init__()
        self.layer1 = nn.Linear(1, 64)
        self.output = nn.Linear(64, 3)

        self.rewards = []
        self.saved_log_probs = []

    def forward(self, x):
        x = F.relu(self.layer1(x))
        action_scores = self.output(x)
        return F.softmax(action_scores, dim=-1)

if __name__ == "__main__":
    policy = Agent()
    optimizer = optim.Adam(policy.parameters(), lr=1e-2)
    print(policy.forward(Variable(torch.from_numpy(np.array([0.1])).float().unsqueeze(0))))
