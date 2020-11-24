from data.datasets import StatsDatasetClassification
from models.mlp_net import MLPNet
from trainer.classification_trainer import ClassificationTrainer
import visualizer
import pandas as pd
import torch

# -------------------------------------------------------------------------------
# This file trains and tests performance of the MLP-network on the simple dataset
# -------------------------------------------------------------------------------

# MODEL VARIABLES
MODEL = MLPNet(10, 6, 3)
TRAINING_SET = StatsDatasetClassification(pd.read_csv("../../data/datasets/processed/simple_train_data.csv"))
TESTING_SET = StatsDatasetClassification(pd.read_csv("../../data/datasets/processed/simple_test_data.csv"))
EPOCHS = 300
LEARNING_RATE = 0.005
OPTIMIZER = torch.optim.SGD(MODEL.parameters(), lr=LEARNING_RATE)
LOSS = torch.nn.CrossEntropyLoss()

if __name__ == '__main__':
    trainer = ClassificationTrainer(MODEL, TRAINING_SET, TESTING_SET, EPOCHS, OPTIMIZER, LOSS)
    trainer.train()
    trainer.print_best_results()
    visualizer.plot_accuracy(trainer.epochs, trainer.val_accuracy, "../../results/graphs/accuracy/simple_mlp_acc.png")
    visualizer.plot_loss(trainer.epochs, trainer.val_loss, "../../results/graphs/loss/simple_mlp_loss.png")

