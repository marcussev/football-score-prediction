from abc import abstractmethod

import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset

'''
This class is used to handle the processed team stats dataset. Inherits from pytorch Dataset.
'''


class StatsDataset(Dataset):

    def __init__(self, filename):
        self.data = pd.read_csv("data/datasets/processed/" + filename)
        self.teams = self.data[["teamA", "teamB"]]
        self.data = self.data.drop(["teamA", "teamB"], axis=1)
        self.game_stats = torch.tensor(self.data.iloc[:, 3:].values, dtype=torch.float)
        self.results = torch.tensor(self.data.iloc[:, 1:3].values)

    def __len__(self):
        return len(self.data)

    @abstractmethod
    def __getitem__(self, index):
        raise NotImplementedError

    def get_teams_by_index(self, index):
        return self.teams.iloc[index]


class StatsDatasetRegression(StatsDataset):
    def __init__(self, filename):
        super().__init__(filename)

    def __getitem__(self, index):
        x_data = self.game_stats[index]
        y_data = self.results[index]
        return x_data, y_data


class StatsDatasetClassification(StatsDataset):
    def __init__(self, filename):
        super().__init__(filename)

    def __getitem__(self, index):
        x_data = self.game_stats[index]
        if self.results[index][0].item() > self.results[index][1].item():
            y_data = torch.tensor([1, 0, 0])
        elif self.results[index][0].item() < self.results[index][1].item():
            y_data = torch.tensor([0, 0, 1])
        else:
            y_data = torch.tensor([0, 1, 0])

        return x_data, y_data
