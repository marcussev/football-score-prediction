import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset

'''
This class is used to handle the processed team stats dataset. Inherits from pytorch Dataset.
'''


class TeamStats(Dataset):

    def __init__(self, filename, transform, target):
        self.data = pd.read_csv("./datasets/processed/" + filename)
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        game_stats = self.data.drop(["A_scored", "B_scored"], axis=1).iloc[index, 1:]
        result = self.data[["A_scored", "B_scored"]].iloc[index]
        return game_stats, result


if __name__ == '__main__':
    dataset = TeamStats("game_stats.csv", None, None)
    print(len(dataset))
    print(dataset.__getitem__(80))
