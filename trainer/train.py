from models.linear_regression import LinearRegression 
from models.mlp_net import MLPNet
from data.datasets import StatsDatasetRegression, StatsDatasetClassification
from .regression_trainer import RegressionTrainer
from .classification_trainer import ClassificationTrainer
from api import db
import pandas as pd
import torch
from utils import BASE_PATH


def train_regression_model():
    model = LinearRegression(18, 2)
    raw_data = db.get_all_raw_data()
    training_data, testing_data = process_raw_data(raw_data, 0.75)
    training_set, testing_set = StatsDatasetRegression(training_data), StatsDatasetRegression(testing_data)

    epochs = 500
    learning_rate = 0.0001
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    loss = torch.nn.MSELoss()

    trainer = RegressionTrainer(model, training_set, testing_set, epochs, optimizer, loss)
    trainer.train()
    trainer.print_best_results()
    trainer.save_model(BASE_PATH + "state_dicts/regression_model.pt")

def train_mlp_model():
    model = MLPNet(18, 6, 3)
    raw_data = db.get_all_raw_data()
    training_data, testing_data = process_raw_data(raw_data, 0.75)
    training_set, testing_set = StatsDatasetClassification(training_data), StatsDatasetClassification(testing_data)
    epochs = 300
    learning_rate = 0.002
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    loss = torch.nn.CrossEntropyLoss()

    trainer = ClassificationTrainer(model, training_set, testing_set, epochs, optimizer, loss)
    trainer.train()
    trainer.print_best_results()
    trainer.save_model(BASE_PATH + "state_dicts/mlp_model.pt")


def process_raw_data(raw, trainDistribution):
    raw = pd.DataFrame(raw)
    data = raw[[
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

    divider = int(len(data) * trainDistribution)
    training_data, testing_data = data[:divider], data[divider:]
    return training_data, testing_data