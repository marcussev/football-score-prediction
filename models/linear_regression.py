from abc import ABC
import torch.nn as nn
import torch

"""
* This is an implementation of a simple linear regression model
"""


class LinearRegression(nn.Module, ABC):
    def __init__(self, input_size, output_size):
        super(LinearRegression, self).__init__()
        self.layer = nn.Linear(input_size, output_size)

    def forward(self, x):
        return self.layer(x)


if __name__ == '__main__':
    model = LinearRegression(10, 2)
    x = torch.tensor([3.0] * 10)
    output = model(x)
    output = [int(output[0]), int(output[1])]
    print(output)
