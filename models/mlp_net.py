from abc import ABC
import torch.nn as nn

# -----------------------------------------------------------------------------
# This file contains an implementation of a Multilayer Perceptron Neural Network
# -----------------------------------------------------------------------------


class MLPNet(nn.Module, ABC):
    def __init__(self, input_size, hidden1_size, hidden2_size):
        super(MLPNet, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden1_size)  # input layer
        self.layer2 = nn.Linear(hidden1_size, hidden2_size)  # hidden layer
        self.layer3 = nn.Linear(hidden2_size, 3)  # output layer
        self.sigmoid = nn.Sigmoid()  # activation function

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return self.sigmoid(x)
