import pandas as pd
import numpy as np
import torch

'''
This class is used to handle the raw datasets that are being used in this project
'''
class Dataloader:

    # Constructor loads the datasets and splits into training and test data
    def __init__(self, data_url):
        self.data = np.array_split(pd.read_csv("../datasets/epl2020.csv"), 2)
        self.training_set
        self.test_set = self.data[1]

    # returns the x-values for the training data
    # Features x-data:
    # [team:[Home/away(1,0), xG, xGA, possession], opponent:[home/away, xG, xGA, possession]]
    def get_x_train(self):
        main_team_data = self.training_set[[]]
        x_train = torch.tensor(np.vstack((self.training_set)))

    # returns the y-values for the training data
    # y-data: ["goals scored", "goals conceded"]
    def get_y_train(self):
        y_train = torch.tensor(np.vstack((self.training_set["scored"], self.training_set["missed"])).T)
        return y_train



if __name__ == '__main__':
    dataloader = Dataloader()
    data = dataloader.training_set
    print(dataloader.get_score(dataloader.get_training_data()[0]))
