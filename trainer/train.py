from models.linear_regression import LinearRegression 
from data.datasets import StatsDatasetRegression
from .regression_trainer import RegressionTrainer
from api import db
import pandas as pd
import torch
from utils import BASE_PATH


def train_regression_model():
    model = LinearRegression(18, 2)
    raw_data = pd.DataFrame(db.get_all_raw_data())
    data = raw_data[[
        "Unnamed: 0", 
        "teamA", 
        "teamB",
        "A_scored",
        "B_scored",
        "A_xG",
        "B_xG",
        "A_xGA",
        "B_xGA",
        "A_ppg",
        "B_ppg",
        "A_gpg",
        "B_gpg",
        "A_cpg",
        "B_cpg",
        "A_deep",
        "B_deep",
        "A_deep_allowed",
        "B_deep_allowed",
        "A_ppda",
        "B_ppda",
        "A_ppda_allowed",
        "B_ppda_allowed",
        ]]

    divider = int(len(data) * 0.75)
    training_data, testing_data = data[:divider], data[divider:]
    training_set, testing_set = StatsDatasetRegression(training_data), StatsDatasetRegression(testing_data)

    epochs = 500
    learning_rate = 0.001
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    loss = torch.nn.MSELoss()

    trainer = RegressionTrainer(model, training_set, testing_set, epochs, optimizer, loss)
    trainer.train()
    trainer.print_best_results()
    trainer.save_model(BASE_PATH + "state_dicts/regression_model.pt")


train_regression_model()