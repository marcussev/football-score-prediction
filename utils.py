import os

# --------------------------------------------------------------------
# This file contains some general helper methods reused in the project
# --------------------------------------------------------------------

# Base path for all datasets
# Change this to your own working directory
BASE_PATH = 'C:/Users/seval/football-score-prediction/'


# save a dataset as csv to given path
def save_as_csv(data, path):
    data.to_csv(BASE_PATH + path)


# save dataset as excel to given path
def save_as_excel(data, path):
    data.to_excel(BASE_PATH + path)


# color cell of a dataframe based on result
def color_cell(val):
    color = "green" if val == "V" else "red"
    return "background-color: %s" % color