from abc import ABC
import torch.nn as nn
import torch

# -----------------------------------------------------------------------
# This file contains a simple implementation of a linear regression model
# -----------------------------------------------------------------------


class LinearRegression(nn.Module, ABC):
    def __init__(self, input_size, output_size):
        super(LinearRegression, self).__init__()
        self.layer = nn.Linear(input_size, output_size)  # linear layer

    def forward(self, x):
        return self.layer(x)
