from data.datasets import StatsDatasetRegression
from models.linear_regression import LinearRegression
from trainer.regression_trainer import RegressionTrainer

import torch

MODEL = LinearRegression(10, 2)
TRAINING_SET = StatsDatasetRegression("games_train_data.csv")
TESTING_SET = StatsDatasetRegression("games_test_data.csv")
EPOCHS = 500
LEARNING_RATE = 0.002
OPTIMIZER = torch.optim.SGD(MODEL.parameters(), lr=LEARNING_RATE)
LOSS = torch.nn.MSELoss()

if __name__ == '__main__':
    trainer = RegressionTrainer(MODEL, TRAINING_SET, TESTING_SET, EPOCHS, OPTIMIZER, LOSS)
    trainer.train()
    trainer.visualize_loss()
    trainer.visualize_accuracy()
    trainer.print_best_results()


