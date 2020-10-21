import pandas as pd

'''
* This file can be ran to convert the raw data from epl2020.csv to a suitable format for this project
* It saves a new file called data.csv to the dataset-folder(data/datasets/data.csv)
* By creating a new separate file we avoid having to run the conversion every time we run the project
'''


def convert_data():
    # Load raw data
    raw_data = pd.read_csv("./datasets/epl2020.csv").rename(
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
    #print(results)

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
    results.loc[results['round'] == 1, ['A_tot_points', 'B_tot_points', 'A_tot_goal', 'B_tot_goal', 'A_tot_con',
                                        'B_tot_con']] = 0
    results['A_tot_points'][2:] = results['A_tot_points'][1:len(results['A_tot_points']) - 1]
    #print(results[results['round'] == 10])

    # Update expected goals so that it is the average of previous games for each team
    teams = results['teamA'].unique()

    for i in range(0, len(teams)):
        team_games = results[results['teamA'] == teams[i]]
        for y in range(0, len(team_games)):
            results[results['teamA'] == teams[i]]['A_xG'] = calculate_average_xg(results, teams[i], y+1)

    print(results[results['teamA'] == "Liverpool"])
    '''
    # Remove non interesting columns
    converted_data = raw_data[["match_id", "teamId", "h_a", "xG", "xGA", "scored", "conceded",
                               "tot_points", "tot_goal", "tot_con", "round"]]

    # Reformat fields with totals to averages
    converted_data["tot_points"] = converted_data["tot_points"] / converted_data["round"]
    converted_data.rename(index=int, columns={"tot_points": "ppg"})
    print(converted_data)
    '''


# Calculate averages for given metric of given games
def calculate_average_xg(data, team, round):
    home_games = data[data['teamA'] == team][0:round-1]
    away_games = data[data['teamB'] == team][0:round-1]
    print(team + ": " + str((home_games['A_xG'].mean() + away_games['B_xG'].mean())/2))
    return (home_games['A_xG'].mean() + away_games['B_xG'].mean())/2


convert_data()
