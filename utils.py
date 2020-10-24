"""
* This file contains general functions that are reused throughout the project
"""

# Base path for all datasets
BASE_PATH = 'C:/Users/seval/PycharmProjects/football-score-prediction/data/datasets/'


# save a dataset as csv to given path
def save_as_csv(data, path):
    data.to_csv(BASE_PATH + path)
