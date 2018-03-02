import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.autograd import Variable
from torch.distributions import Categorical


class Agent(nn.Module):

    def __init__(self):
        super(Agent, self).__init__()
        self.layer1 = nn.Linear(4, 64)
        self.layer2 = nn.Linear(64, 32)
        self.output = nn.Linear(32, 2)

        self.rewards = []
        self.saved_log_probs = []

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        action_scores = self.output(x)
        return F.softmax(action_scores, dim=-1)
