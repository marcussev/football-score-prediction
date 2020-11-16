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
        df = df.style.applymap(utils.color_cell, subset=["correct"])
        utils.save_as_excel(df, "results/regression_results.xlsx")
        print(df)

    def get_result(self, score):
        team_a_score = round(score[0][0].item())
        team_b_score = round(score[0][1].item())
        if team_a_score > team_b_score:
            return 1
        elif team_a_score == team_b_score:
            return 0
        else:
            return -1

    def get_epoch_results(self, teams, predicted, actual, correct):
        return [teams[0], teams[1], "%s-%s" % (round(predicted[0][0].item()), round(predicted[0][1].item())),
                "%s-%s" % (round(actual[0][0].item()), round(actual[0][1].item())), correct]
