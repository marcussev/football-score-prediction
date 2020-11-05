from data.datasets import StatsDatasetClassification
from models.mlp_net import MLPNet
from trainer.classification_trainer import ClassificationTrainer

import torch

MODEL = MLPNet(10, 6, 3)
TRAINING_SET = StatsDatasetClassification("games_train_data.csv")
TESTING_SET = StatsDatasetClassification("games_test_data.csv")
EPOCHS = 400
LEARNING_RATE = 0.07
OPTIMIZER = torch.optim.SGD(MODEL.parameters(), lr=LEARNING_RATE)
LOSS = torch.nn.MSELoss()

if __name__ == '__main__':
    trainer = ClassificationTrainer(MODEL, TRAINING_SET, TESTING_SET, EPOCHS, OPTIMIZER, LOSS)
    trainer.train()
    trainer.visualize_loss()
    trainer.visualize_accuracy()
    trainer.print_best_results()
