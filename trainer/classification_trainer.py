from trainer.trainer import Trainer
import utils
import pandas as pd
import torch

# ------------------------------------------------
# This file contains class for training MLP-models
# Class inherits from base Trainer class
# ------------------------------------------------


class ClassificationTrainer(Trainer):
    def __init__(self, model, training_set, testing_set, epochs, optimizer, loss):
        super().__init__(model, training_set, testing_set, epochs, optimizer, loss)

    def calculate_loss(self, output, y):
        return self.loss(output, torch.max(y, 1)[1])

    def print_best_results(self):
        df = pd.DataFrame(self.best_results, columns=["teamA", "teamB", "predictedWinner", "actualWinner", "correct"])
        print(df)

    def get_result(self, score):
        # team A win has highest value
        if torch.argmax(score) == 0:
            return 1

        # team B win has highest value
        elif torch.argmax(score) == 1:
            return 0

        # draw has highest value
        else:
            return -1

    def get_epoch_results(self, teams, predicted, actual, correct):
        predicted_winner = self.get_winner(teams, predicted)
        actual_winner = self.get_winner(teams, actual)
        return [teams[0], teams[1], predicted_winner, actual_winner, correct]

    # Method for determining name of winning team
    def get_winner(self, teams, outcome):
        if self.get_result(outcome) == 1:
            winner = teams[0]
        elif self.get_result(outcome) == -1:
            winner = teams[1]
        else:
            winner = "Draw"
        return winner
