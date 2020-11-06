"""
* This file contains general functions that are reused throughout the project
"""

# Base path for all datasets
BASE_PATH = 'C:/Users/seval/PycharmProjects/football-score-prediction/'


# save a dataset as csv to given path
def save_as_csv(data, path):
    data.to_csv(BASE_PATH + path)


# color cell of a dataframe based on result
def color_cell(val):
    color = "green" if val == "V" else "red"
    return "background-color: %s" % color
