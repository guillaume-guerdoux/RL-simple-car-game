import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class Agent(nn.Module):

    def __init__(self):
        super(Agent, self).__init__()
        self.layer1 = nn.Linear(1, 32)
        self.output = nn.Linear(32, 2)

        self.rewards = []
        self.saved_log_probs = []

    def forward(self, x):
        x = F.relu(self.layer1(x))
        action_scores = self.output(x)
        print(action_scores)
        return F.softmax(action_scores, dim=-1)
