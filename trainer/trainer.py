import math

from torch.utils.data import dataloader
import copy
import torch

"""
* Trainer is a class that can be used to train different models given different model and training variables
"""


class Trainer:
    def __init__(self, model, training_set, testing_set, epochs, optimizer, loss, learning_rate):
        # Training variables
        self.model = model
        self.epochs = epochs
        self.optimizer = optimizer
        self.loss = loss
        self.learning_rate = learning_rate

        # Training and testing data as Dataset-objects
        self.training_set = training_set
        self.testing_set = testing_set

        # Using DataLoader to load the datasets
        self.training_data = dataloader.DataLoader(training_set)
        self.testing_set = dataloader.DataLoader(testing_set)

        # Containers for visualizing loss
        self.train_loss = []
        self.val_loss = []

        # Best model during training
        self.best_model = copy.deepcopy(self.model)
        self.best_loss = float("inf")
        self.best_accuracy = 0.0  # 100.0 = 100%, 0.0 = 0%

    def train(self):
        for i in range(self.epochs):
            correct_predictions = 0  # counter for correct predictions
            for train_batch in self.training_data:
                x, y = train_batch
                output = self.model(x)
                loss = self.loss(output, y)
                self.train_loss.append(loss)

                # Remember model state if it is the current best
                if loss.item() < self.best_loss:
                    self.best_model = copy.deepcopy(self.model)
                    self.best_loss = loss.item()

                # Check if model predicted right winner
                # pred_winner =
                # val_winner =

                # Optimize model
                loss.backward()
                self.optimizer.step()
                self.optimizer.zero_grad()

            self.accuracy()

    def validate(self):
        with torch.no_grad():
            raise NotImplementedError

    def accuracy(self):
        raise NotImplementedError

    def visualize_accuracy(self):
        raise NotImplementedError

    def visualize_loss(self):
        raise NotImplementedError
