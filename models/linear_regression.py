from abc import ABC
import torch.nn as nn

"""
* This is an implementation of a simple linear regression model
"""


class LinearRegression(nn.Module, ABC):
    def __init__(self, input_size, output_size):
        super(LinearRegression, self).__init__()
        self.layer = nn.Linear(input_size, output_size)

    def forward(self, x):
        return self.layer(x)
