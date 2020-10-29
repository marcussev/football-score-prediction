import math

from torch.utils.data import dataloader
import copy
import torch

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
                loss = self.loss(output.float(), y.float())
                self.train_loss.append(loss)

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

            # Calculate and print accuracy on training data
            print("Epoch %s:\nTraining accuracy: %s%s" % (
                i, self.accuracy(correct_predictions, len(self.training_set)), "%"))

            # Run model on test data to validate performance
            test_accuracy = self.validate()
            print("Testing accuracy: ", test_accuracy, "%\n")

    def validate(self):
        with torch.no_grad():
            correct_predictions = 0
            for test_batch in self.testing_data:
                x, y = test_batch
                output = self.model(x)
                self.val_loss.append(self.loss(output, y))
                pred_result = self.get_result(output)
                val_result = self.get_result(y)
                if pred_result == val_result:
                    correct_predictions += 1
            return self.accuracy(correct_predictions, len(self.testing_set))

    def visualize_accuracy(self):
        raise NotImplementedError

    def visualize_loss(self):
        raise NotImplementedError

    @staticmethod
    def accuracy(correct_predictions, predictions):
        acc = (correct_predictions / predictions) * 100
        return round(acc, 2)

    # determines the match result based on scores, returns 0 for draw, -1 for teamB win and +1 for teamA win
    @staticmethod
    def get_result(score):
        team_a_score = int(score[0][0])
        team_b_score = int(score[0][1])
        if team_a_score > team_b_score:
            return 1
        elif team_a_score == team_b_score:
            return 0
        else:
            return -1

