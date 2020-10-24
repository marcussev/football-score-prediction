import pandas as pd
from itertools import islice

'''
* This file can be ran to convert the raw data from epl2020.csv to a suitable format for this project
* It saves a new file called data.csv to the dataset-folder(data/datasets/data.csv)
* By creating a new separate file we avoid having to run the conversion every time we run the project
'''


def convert_data():
    # Load raw data
    raw_data = pd.read_csv("datasets/raw/epl2020.csv").rename(
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
    results = raw_data.groupby(by=['Referee.x', 'date']).agg({'teamId': ','.join,
                                                              'scored': ','.join,
                                                              'xG': ','.join,
                                                              'xGA': ','.join,
                                                              'tot_points': ",".join,
                                                              'tot_goal': ",".join,
                                                              'tot_con': ",".join,
                                                              'round': 'max'
                                                              }).reset_index()
    # print(results)

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

    results.sort_values(by='date', inplace=True)
    results.reset_index(inplace=True, drop=True)

    # Remove all other columns
    results = results[['round', 'teamA', 'teamB', 'A_scored', 'B_scored', 'A_xG', 'B_xG', 'A_xGA',
                       'B_xGA', 'A_tot_points', 'B_tot_points', 'A_tot_goal', 'B_tot_goal',
                       'A_tot_con', 'B_tot_con']]

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
    results.rename(index=int, columns={"A_tot_points": 'A_ppg', 'B_tot_points': 'B_ppg', 'A_tot_goal': 'A_gpg',
                                       'B_tot_goal': 'B_gpg', 'A_tot_con': 'A_cpg', 'B_tot_con': 'B_cpg'})

    # Update rows so that it has average values from previous games
    for i, row in results.iterrows():
        results.loc[i, 'A_xG'] = calculate_average_xg(results, row['teamA'], row['round'], 'xG')
        results.loc[i, 'B_xG'] = calculate_average_xg(results, row['teamB'], row['round'], 'xG')
        results.loc[i, 'A_xGA'] = calculate_average_xg(results, row['teamA'], row['round'], 'xGA')
        results.loc[i, 'B_xGA'] = calculate_average_xg(results, row['teamB'], row['round'], 'xGA')

    print(results[(results['teamA'] == "Liverpool") | (results['teamB'] == 'Liverpool')])


def save_as_csv(data, filename):
    data.to_csv()


# Calculate averages for given metric of given games
def calculate_average_xg(data, team, round, metric):
    home_games = data[data['teamA'] == team][0:round - 1]
    away_games = data[data['teamB'] == team][0:round - 1]
    return (home_games['A_' + metric].mean() + away_games['B_' + metric].mean()) / 2


def calculate_average_totals(row):
    if row['round'] != 1:
        row['A_tot_points'] = row['A_tot_points'] / (row['round'] - 1)
        row['A_tot_goal'] = row['A_tot_goal'] / (row['round'] - 1)
        row['A_tot_con'] = row['A_tot_con'] / (row['round'] - 1)
        row['B_tot_points'] = row['B_tot_points'] / (row['round'] - 1)
        row['B_tot_goal'] = row['B_tot_goal'] / (row['round'] - 1)
        row['B_tot_con'] = row['B_tot_con'] / (row['round'] - 1)
    return row


convert_data()
