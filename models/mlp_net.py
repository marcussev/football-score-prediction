from abc import ABC

import torch
import torch.nn as nn

"""
* This is an implementation of a simple multilayer perception neural net (MLP)
"""


class MLPNet(nn.Module, ABC):
    def __init__(self, input_size, hidden1_size, hidden2_size):
        super(MLPNet, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden1_size)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(hidden1_size, hidden2_size)
        self.layer3 = nn.Linear(hidden2_size, 3)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)
        x = self.relu(x)
        x = self.layer3(x)
        return self.sigmoid(x)
