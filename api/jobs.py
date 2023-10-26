import datascraper
import db
import sys
sys.path.append('../')
from predictor import Predictor
import torch

def update_team_stats(league, only_newest):
    teams = datascraper.get_latest_stats(league, '2023')
    response = db.update_all_teams(league, teams)
    print(response)

def update_gameweeks(league, season):
    gameweeks = datascraper.get_all_gameweeks(league, season)
    response = db.update_all_gameweeks(league, '2023', gameweeks)
    print(response)

def update_predictions(league, season, gameweek):
    predictor = Predictor()

    games = db.get_gameweek(league, season, gameweek)
    for game_id in games['matches']:
        game = games['matches'][game_id]
        
        home_team_stats = db.get_team(league, game['home'])
        away_team_stats = db.get_team(league, game['away'])

        input_data = {
            "A_xG": home_team_stats['xG'],
            "B_xG": away_team_stats['xG'],
            "A_xGA": home_team_stats['xGA'],
            "B_xGA": away_team_stats['xGA'],
            "A_ppg": home_team_stats['ppg'],
            "B_ppg": away_team_stats['ppg'],
            "A_gpg": home_team_stats['gpg'],
            "B_gpg": away_team_stats['gpg'],
            "A_cpg": home_team_stats['cpg'],
            "B_cpg": away_team_stats['cpg'],
            "A_deep": home_team_stats['deep'],
            "B_deep": away_team_stats['deep'],
            "A_deep_allowed": home_team_stats['deep_allowed'],
            "B_deep_allowed": away_team_stats['deep_allowed'],
            "A_ppda": home_team_stats['ppda'],
            "B_ppda": away_team_stats['ppda'],
            "A_ppda_allowed": home_team_stats['ppda_allowed'],
            "B_ppda_allowed": away_team_stats['ppda_allowed'],
        }

        predicted_result = predictor.predict_result(torch.tensor(list(input_data.values()), dtype=torch.float))
        print(game['home'] + ' vs ' + game['away'])
        print(predicted_result)

update_predictions('epl', '2023', '9')