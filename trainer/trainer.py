import math
from abc import abstractmethod

from torch.utils.data import dataloader
import copy
import torch
import visualizer
import pandas as pd

"""
* Trainer is a class that can be used to train different models given different model and training variables
"""


class Trainer:
    def __init__(self, model, training_set, testing_set, epochs, optimizer, loss):
        # Training variables
        self.model = model
        self.epochs = epochs
        self.optimizer = optimizer
        self.loss = loss

        # Training and testing data as Dataset-objects
        self.training_set = training_set
        self.testing_set = testing_set

        # Using DataLoader to load the datasets
        self.training_data = dataloader.DataLoader(training_set)
        self.testing_data = dataloader.DataLoader(testing_set)

        # Containers for visualizing
        self.train_loss = []
        self.val_loss = []
        self.val_accuracy = []

        # Best model during training
        self.best_model = copy.deepcopy(self.model)
        self.best_loss = float("inf")
        self.best_accuracy = 0.0  # 100.0 = 100%, 0.0 = 0%
        self.best_results = []  # list containing all results from best prediction

    def train(self):
        for i in range(self.epochs):
            correct_predictions = 0  # counter for correct predictions
            epoch_loss = []
            for train_batch in self.training_data:
                x, y = train_batch
                output = self.model(x)
                loss = self.loss(output.float(), y.float())
                epoch_loss.append(loss)

                # Remember model state if it is the current best
                if loss.item() < self.best_loss:
                    self.best_model = copy.deepcopy(self.model)
                    self.best_loss = loss.item()

                # Check if model predicted right winner
                pred_result = self.get_result(output)
                val_result = self.get_result(y)
                if pred_result == val_result:
                    correct_predictions += 1

                # Optimize model
                loss.backward()
                self.optimizer.step()
                self.optimizer.zero_grad()

            self.train_loss.append(sum(epoch_loss) / len(epoch_loss))

            # Calculate and print accuracy on training data
            print("Epoch %s:\nTraining accuracy: %s%s" % (
                i, self.accuracy(correct_predictions, len(self.training_set)), "%"))

            # Run model on test data to validate performance
            test_accuracy = self.validate()
            self.val_accuracy.append(test_accuracy)
            print("Testing accuracy: ", test_accuracy, "%\n")

    def validate(self):
        with torch.no_grad():
            correct_predictions = 0  # how many games was the right winner predicted
            epoch_loss = []  # loss for current epoch
            game_index = 0
            epoch_results = []  # list of game results from current epoch
            for test_batch in self.testing_data:
                correct = "X"
                x, y = test_batch
                output = self.model(x)
                epoch_loss.append(self.loss(output, y))
                pred_result = self.get_result(output)
                val_result = self.get_result(y)
                if pred_result == val_result:
                    correct_predictions += 1
                    correct = "V"
                teams = self.testing_set.get_teams_by_index(game_index)
                game_index += 1
                epoch_results.append(self.get_epoch_results(teams, output, y, correct))

            # add epoch loss
            self.val_loss.append(sum(epoch_loss) / len(epoch_loss))

            # check if this is the current most accurate prediction
            epoch_accuracy = self.accuracy(correct_predictions, len(self.testing_set))
            if epoch_accuracy > self.best_accuracy:
                self.best_results = epoch_results
                self.best_accuracy = epoch_accuracy
            return epoch_accuracy

    def visualize_accuracy(self):
        visualizer.plot_accuracy(self.epochs, self.val_accuracy)

    def visualize_loss(self):
        visualizer.plot_loss(self.epochs, self.val_loss)

    @abstractmethod
    def print_best_results(self):
        raise NotImplementedError

    # determines the match result based on scores, returns 0 for draw, -1 for teamB win and +1 for teamA win
    @abstractmethod
    def get_result(self, score):
        raise NotImplementedError

    @abstractmethod
    def get_epoch_results(self, teams, predicted, actual, correct):
        raise NotImplementedError

    @staticmethod
    def accuracy(correct_predictions, predictions):
        acc = (correct_predictions / predictions) * 100
        return round(acc, 2)

