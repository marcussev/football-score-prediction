from data.team_stats import TeamStats
from models.linear_regression import LinearRegression
from trainer.trainer import Trainer

import torch

MODEL = LinearRegression(10, 2)
TRAINING_SET = TeamStats("games_train_data.csv")
TESTING_SET = TeamStats("games_test_data.csv")
EPOCHS = 100
LEARNING_RATE = 0.01
OPTIMIZER = torch.optim.SGD(MODEL.parameters(), lr=LEARNING_RATE)
LOSS = torch.nn.MSELoss()

if __name__ == '__main__':
    trainer = Trainer(MODEL, TRAINING_SET, TESTING_SET, EPOCHS, OPTIMIZER, LOSS)
    trainer.train()


