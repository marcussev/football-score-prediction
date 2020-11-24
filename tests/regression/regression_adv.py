from data.datasets import StatsDatasetRegression
from models.linear_regression import LinearRegression
from trainer.regression_trainer import RegressionTrainer
import visualizer
import pandas as pd
import torch

# ---------------------------------------------------------------------------------------------
# This file trains and tests performance of the linear regression model on the advanced dataset
# ---------------------------------------------------------------------------------------------

# MODEL VARIABLES
MODEL = LinearRegression(18, 2)
TRAINING_SET = StatsDatasetRegression(pd.read_csv("../../data/datasets/processed/adv_train_data.csv"))
TESTING_SET = StatsDatasetRegression(pd.read_csv("../../data/datasets/processed/adv_test_data.csv"))
EPOCHS = 500
LEARNING_RATE = 0.001
OPTIMIZER = torch.optim.SGD(MODEL.parameters(), lr=LEARNING_RATE)
LOSS = torch.nn.MSELoss()

if __name__ == '__main__':
    trainer = RegressionTrainer(MODEL, TRAINING_SET, TESTING_SET, EPOCHS, OPTIMIZER, LOSS)
    trainer.train()
    trainer.print_best_results()
    visualizer.plot_accuracy(trainer.epochs, trainer.val_accuracy, "../../results/graphs/accuracy/adv_reg_acc.png")
    visualizer.plot_loss(trainer.epochs, trainer.val_loss, "../../results/graphs/loss/adv_reg_loss.png")



