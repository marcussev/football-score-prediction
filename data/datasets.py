from abc import abstractmethod
import torch
from torch.utils.data import Dataset


# ---------------------------------------------------------------------------
# This file contains classes for Datasets
# These are used to create Dataset objects that can be loaded by Dataloaders
# ---------------------------------------------------------------------------


# This the parent Dataset class for this project inheriting from pytorch Dataset
class StatsDataset(Dataset):

    # Dataset is separated into teams, stats and results
    def __init__(self, dataset):
        self.data = dataset
        self.teams = self.data[["teamA", "teamB"]]  # Names of the two teams in given game
        self.data = self.data.drop(["teamA", "teamB"], axis=1)  # Team names can not be in actual data
        self.game_stats = torch.tensor(self.data.iloc[:, 3:].values, dtype=torch.float)  # Model X, historic stats
        self.results = torch.tensor(self.data.iloc[:, 1:3].values)  # Model y, goals scored by each team

    def __len__(self):
        return len(self.data)

    @abstractmethod
    # Method for getting x-data and y-data from each game
    # Implemented in child classes
    def __getitem__(self, index):
        raise NotImplementedError

    def get_teams_by_index(self, index):
        return self.teams.iloc[index]


# Child Dataset class specifically for regression models
class StatsDatasetRegression(StatsDataset):
    def __init__(self, filename):
        super().__init__(filename)

    def __getitem__(self, index):
        x_data = self.game_stats[index]  # Historic stats for given game
        y_data = self.results[index]  # Both team scores for given game
        return x_data, y_data


# Child Dataset class specifically for classification models
class StatsDatasetClassification(StatsDataset):
    def __init__(self, filename):
        super().__init__(filename)

    def __getitem__(self, index):
        x_data = self.game_stats[index]  # Historic stats for given game

        # if team A is winner
        if self.results[index][0].item() > self.results[index][1].item():
            y_data = torch.tensor([1, 0, 0])

        # if team B is winner
        elif self.results[index][0].item() < self.results[index][1].item():
            y_data = torch.tensor([0, 0, 1])

        # if game result is draw
        else:
            y_data = torch.tensor([0, 1, 0])

        return x_data, y_data
