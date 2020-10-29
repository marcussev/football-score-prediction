import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset

'''
This class is used to handle the processed team stats dataset. Inherits from pytorch Dataset.
'''


class TeamStats(Dataset):

    def __init__(self, filename):
        self.data = pd.read_csv("data/datasets/processed/" + filename)
        self.teams = self.data[["teamA", "teamB"]]
        self.data = self.data.drop(["teamA", "teamB"], axis=1)

        self.game_stats = torch.tensor(self.data.iloc[:, 3:].values, dtype=torch.float)
        self.results = torch.tensor(self.data.iloc[:, 1:3].values)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        x_data = self.game_stats[index]
        y_data = self.results[index]
        return x_data, y_data

    def get_teams_by_index(self, index):
        return self.teams.iloc[index]


if __name__ == '__main__':
    dataset = TeamStats("games_train_data.csv")
    print(dataset)
    print(len(dataset.__getitem__(90)[0]))
    print(dataset.get_teams_by_index(90))
