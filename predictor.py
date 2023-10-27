from models.linear_regression import LinearRegression
from models.mlp_net import MLPNet
import torch
from utils import BASE_PATH

class RegressionPredictor():
    def __init__(self):
        self.model = LinearRegression(18, 2)
        self.model.load_state_dict(torch.load(BASE_PATH + "state_dicts/regression_model.pt"))
        self.model.eval()

    def predict_result(self, data):
        pred = self.model(data)
        team_a_score = round(pred[0].item())
        team_b_score = round(pred[1].item())
        return [team_a_score, team_b_score]

class MLPPredictor():
    def __init__(self):
        self.model = MLPNet(18, 6, 3)
        self.model.load_state_dict(torch.load(BASE_PATH + "state_dicts/mlp_model.pt"))
        self.model.eval()

    def predict_result(self, data):
        pred = self.model(data)
        # team A win has highest value
        if torch.argmax(pred) == 0:
            return 1

        # team B win has highest value
        elif torch.argmax(pred) == 1:
            return 0

        # draw has highest value
        else:
            return -1
    