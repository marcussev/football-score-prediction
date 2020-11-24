import pandas as pd
import sys

sys.path.append("..")
from utils import save_as_csv


# -------------------------------------------------
# This file consists of methods for processing data
# -------------------------------------------------

# This method loads the raw dataset and processes it to an appropriate format
def process_raw_data():
    # Load raw data
    raw_data = pd.read_csv("data/datasets/raw/epl2020.csv").rename(
        index=int, columns={"Unnamed: 0": "match_id", "missed": "conceded"})

    # Sort entries by date and home/away team
    raw_data.sort_values(by=['date', 'h_a'], inplace=True)
    raw_data.reset_index()

    # Collect all relevant data for both teams from a single game
    raw_data["scored"] = raw_data["scored"].apply(lambda x: str(x))
    raw_data["xG"] = raw_data["xG"].apply(lambda x: str(x))
    raw_data["xGA"] = raw_data["xGA"].apply(lambda x: str(x))
    raw_data["tot_points"] = raw_data["tot_points"].apply(lambda x: str(x))
    raw_data["tot_goal"] = raw_data["tot_goal"].apply(lambda x: str(x))
    raw_data["tot_con"] = raw_data["tot_con"].apply(lambda x: str(x))
    raw_data["deep"] = raw_data["deep"].apply(lambda x: str(x))
    raw_data["deep_allowed"] = raw_data["deep_allowed"].apply(lambda x: str(x))
    raw_data["ppda_cal"] = raw_data["ppda_cal"].apply(lambda x: str(x))
    raw_data["allowed_ppda"] = raw_data["allowed_ppda"].apply(lambda x: str(x))
    results = raw_data.groupby(by=['Referee.x', 'date']).agg({'teamId': ','.join,
                                                              'scored': ','.join,
                                                              'xG': ','.join,
                                                              'xGA': ','.join,
                                                              'tot_points': ",".join,
                                                              'tot_goal': ",".join,
                                                              'tot_con': ",".join,
                                                              'deep': ",".join,
                                                              'deep_allowed': ",".join,
                                                              'ppda_cal': ",".join,
                                                              'allowed_ppda': ",".join,
                                                              'round': 'max'
                                                              }).reset_index()

    # Combine rows so that each game has only one row
    results['teamA'] = results['teamId'].apply(lambda x: x.split(',')[0])
    results['teamB'] = results['teamId'].apply(lambda x: x.split(',')[1])
    results['A_scored'] = results['scored'].apply(lambda x: x.split(',')[0]).astype('uint16')
    results['B_scored'] = results['scored'].apply(lambda x: x.split(',')[1]).astype('uint16')
    results['A_xG'] = results['xG'].apply(lambda x: x.split(',')[0]).astype('float')
    results['B_xG'] = results['xG'].apply(lambda x: x.split(',')[1]).astype('float')
    results['A_xGA'] = results['xGA'].apply(lambda x: x.split(',')[0]).astype('float')
    results['B_xGA'] = results['xGA'].apply(lambda x: x.split(',')[1]).astype('float')
    results['A_tot_points'] = results['tot_points'].apply(lambda x: x.split(',')[0]).astype('uint16')
    results['B_tot_points'] = results['tot_points'].apply(lambda x: x.split(',')[1]).astype('uint16')
    results['A_tot_goal'] = results['tot_goal'].apply(lambda x: x.split(',')[0]).astype('uint16')
    results['B_tot_goal'] = results['tot_goal'].apply(lambda x: x.split(',')[1]).astype('uint16')
    results['A_tot_con'] = results['tot_con'].apply(lambda x: x.split(',')[0]).astype('uint16')
    results['B_tot_con'] = results['tot_con'].apply(lambda x: x.split(',')[1]).astype('uint16')
    results['A_deep'] = results['deep'].apply(lambda x: x.split(',')[0]).astype('uint16')
    results['B_deep'] = results['deep'].apply(lambda x: x.split(',')[1]).astype('uint16')
    results['A_deep_allowed'] = results['deep_allowed'].apply(lambda x: x.split(',')[0]).astype('uint16')
    results['B_deep_allowed'] = results['deep_allowed'].apply(lambda x: x.split(',')[1]).astype('uint16')
    results['A_ppda'] = results['ppda_cal'].apply(lambda x: x.split(',')[0]).astype(float).astype('uint16')
    results['B_ppda'] = results['ppda_cal'].apply(lambda x: x.split(',')[1]).astype(float).astype('uint16')
    results['A_ppda_allowed'] = results['allowed_ppda'].apply(lambda x: x.split(',')[0]).astype(float).astype('uint16')
    results['B_ppda_allowed'] = results['allowed_ppda'].apply(lambda x: x.split(',')[1]).astype(float).astype('uint16')

    results.sort_values(by='date', inplace=True)
    results.reset_index(inplace=True, drop=True)

    # Use only the columns that are interesting
    results = results[['round', 'teamA', 'teamB', 'A_scored', 'B_scored', 'A_xG', 'B_xG', 'A_xGA',
                       'B_xGA', 'A_tot_points', 'B_tot_points', 'A_tot_goal', 'B_tot_goal',
                       'A_tot_con', 'B_tot_con', 'A_deep', 'B_deep', 'A_deep_allowed', 'B_deep_allowed',
                       'A_ppda', 'B_ppda', 'A_ppda_allowed', 'B_ppda_allowed']]

    # Totals needs to be from previous games, not including current game
    # Therefore set all totals from first round to 0, and shift stats backwards 1 round
    res_copy = results.copy()
    for i, row in results[results['round'] > 1].iterrows():
        previous_games = results[:i]
        last_game_a = previous_games.loc[previous_games.where((previous_games['teamA'] == row['teamA']) | (
                previous_games['teamB'] == row['teamA'])).last_valid_index()]
        last_game_b = previous_games.loc[previous_games.where((previous_games['teamA'] == row['teamB']) | (
                previous_games['teamB'] == row['teamB'])).last_valid_index()]

        # Update for teamA
        if last_game_a['teamA'] == row['teamA']:
            res_copy.loc[i, 'A_tot_points'] = last_game_a['A_tot_points']
            res_copy.loc[i, 'A_tot_goal'] = last_game_a['A_tot_goal']
            res_copy.loc[i, 'A_tot_con'] = last_game_a['A_tot_con']
        elif last_game_a['teamB'] == row['teamA']:
            res_copy.loc[i, 'A_tot_points'] = last_game_a['B_tot_points']
            res_copy.loc[i, 'A_tot_goal'] = last_game_a['B_tot_goal']
            res_copy.loc[i, 'A_tot_con'] = last_game_a['B_tot_con']

        # Update for teamB
        if last_game_b['teamA'] == row['teamB']:
            res_copy.loc[i, 'B_tot_points'] = last_game_b['A_tot_points']
            res_copy.loc[i, 'B_tot_goal'] = last_game_b['A_tot_goal']
            res_copy.loc[i, 'B_tot_con'] = last_game_b['A_tot_con']
        elif last_game_b['teamB'] == row['teamB']:
            res_copy.loc[i, 'B_tot_points'] = last_game_b['B_tot_points']
            res_copy.loc[i, 'B_tot_goal'] = last_game_b['B_tot_goal']
            res_copy.loc[i, 'B_tot_con'] = last_game_b['B_tot_con']

    # Update original data
    results = res_copy

    # Set first round game stats to 0
    results.loc[results['round'] == 1, ['A_tot_points', 'B_tot_points', 'A_tot_goal', 'B_tot_goal', 'A_tot_con',
                                        'B_tot_con']] = 0

    # Convert totals to averages
    results = results.apply(lambda x: calculate_average_totals(x), axis=1)
    results = results.rename(index=int,
                             columns={"A_tot_points": 'A_ppg', 'B_tot_points': 'B_ppg', 'A_tot_goal': 'A_gpg',
                                      'B_tot_goal': 'B_gpg', 'A_tot_con': 'A_cpg', 'B_tot_con': 'B_cpg'})

    # Update rows so that it has average values from previous games
    for i, row in results.iterrows():
        results.loc[i, 'A_xG'] = calculate_average(results, row['teamA'], row['round'], 'xG')
        results.loc[i, 'B_xG'] = calculate_average(results, row['teamB'], row['round'], 'xG')
        results.loc[i, 'A_xGA'] = calculate_average(results, row['teamA'], row['round'], 'xGA')
        results.loc[i, 'B_xGA'] = calculate_average(results, row['teamB'], row['round'], 'xGA')
        results.loc[i, 'A_deep'] = calculate_average(results, row['teamA'], row['round'], 'deep')
        results.loc[i, 'B_deep'] = calculate_average(results, row['teamB'], row['round'], 'deep')
        results.loc[i, 'A_deep_allowed'] = calculate_average(results, row['teamA'], row['round'], 'deep_allowed')
        results.loc[i, 'B_deep_allowed'] = calculate_average(results, row['teamB'], row['round'], 'deep_allowed')
        results.loc[i, 'A_ppda'] = calculate_average(results, row['teamA'], row['round'], 'ppda')
        results.loc[i, 'B_ppda'] = calculate_average(results, row['teamB'], row['round'], 'ppda')
        results.loc[i, 'A_ppda_allowed'] = calculate_average(results, row['teamA'], row['round'], 'ppda_allowed')
        results.loc[i, 'B_ppda_allowed'] = calculate_average(results, row['teamB'], row['round'], 'ppda_allowed')

    return results


# This method converts metrics related to single games
# It calculates averages for given metric based on previous games instead
def calculate_average(data, team, round, metric):
    home_games = data[data['teamA'] == team][0:round - 1]
    away_games = data[data['teamB'] == team][0:round - 1]
    return (home_games['A_' + metric].mean() + away_games['B_' + metric].mean()) / 2


# This method is for converting metrics that are accumulating throughout the season
# It calculates the averages of these metrics from previous games instead
def calculate_average_totals(row):
    if row['round'] != 1:
        row['A_tot_points'] = row['A_tot_points'] / (row['round'] - 1)
        row['A_tot_goal'] = row['A_tot_goal'] / (row['round'] - 1)
        row['A_tot_con'] = row['A_tot_con'] / (row['round'] - 1)
        row['B_tot_points'] = row['B_tot_points'] / (row['round'] - 1)
        row['B_tot_goal'] = row['B_tot_goal'] / (row['round'] - 1)
        row['B_tot_con'] = row['B_tot_con'] / (row['round'] - 1)
    return row


# Helper method to remove last unwanted column from interim state
def process_interim_data(data):
    return data.drop(["round"], axis=1)


# Method to create processed datasets with advanced metrics
# Dataset of interim state as input
def get_advanced_data(data):
    x = data[data["round"] > 2]
    divider = int((len(x) / 100) * 75)
    train = x[:divider]
    test = x[divider:]
    return process_interim_data(train), process_interim_data(test), process_interim_data(x)


# Method to create processed datasets with simple metrics
# Dataset of interim state as input
def get_simplified_data(data):
    x = data[data["round"] > 2]
    x = x.drop(["A_deep", "B_deep", "A_deep_allowed", "B_deep_allowed", "A_ppda", "B_ppda", "A_ppda_allowed",
                "B_ppda_allowed"], axis=1)
    divider = int((len(x) / 100) * 75)
    train = x[:divider]
    test = x[divider:]
    return process_interim_data(train), process_interim_data(test)


# Method to create processed datasets for MLP-models with optimal metrics
# Dataset of interim state as input
def get_optimal_mlp_data(data):
    x = data[data["round"] > 2]
    x = x.drop(["A_ppg", "B_ppg", "A_gpg", "B_gpg", "A_cpg", "B_cpg"], axis=1)
    divider = int((len(x) / 100) * 75)
    train = x[:divider]
    test = x[divider:]
    return process_interim_data(train), process_interim_data(test)


# Method to create processed datasets for regression models with optimal metrics
# Dataset of interim state as input
def get_optimal_reg_data(data):
    x = data[data["round"] > 2]
    x = x[["teamA", "teamB", "A_scored", "B_scored", "A_xG", "B_xG", "A_xGA", "B_xGA"]]
    divider = int((len(x) / 100) * 75)
    train = x[:divider]
    test = x[divider:]
    return train, test

