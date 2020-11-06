import pandas as pd
import utils

from trainer.trainer import Trainer


class RegressionTrainer(Trainer):
    def __init__(self, model, training_set, testing_set, epochs, optimizer, loss):
        super().__init__(model, training_set, testing_set, epochs, optimizer, loss)

    def calculate_loss(self, output, y):
        return self.loss(output.float(), y.float())

    def print_best_results(self):
        df = pd.DataFrame(self.best_results, columns=["teamA", "teamB", "predictedScore", "actualScore", "correct"])
        df.style.apply(utils.color_cell, subset=["correct"])
        utils.save_as_csv(df, "results/regression_results.csv")
        print(df)

    def get_result(self, score):
        team_a_score = int(score[0][0])
        team_b_score = int(score[0][1])
        if team_a_score > team_b_score:
            return 1
        elif team_a_score == team_b_score:
            return 0
        else:
            return -1

    def get_epoch_results(self, teams, predicted, actual, correct):
        return [teams[0], teams[1], "%s-%s" % (int(predicted[0][0]), int(predicted[0][1])),
                "%s-%s" % (int(actual[0][0]), int(actual[0][1])), correct]
