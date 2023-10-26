from models.linear_regression import LinearRegression
import torch
from utils import BASE_PATH

class Predictor():
    def __init__(self):
        self.model = LinearRegression(18, 2)
        self.model.load_state_dict(torch.load(BASE_PATH + "state_dicts/regression_model.pt"))
        self.model.eval()

    def predict_result(self, data):
        return self.model(data)
    