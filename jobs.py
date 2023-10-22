import datascraper
from api.database.leagues import update_all_teams, update_all_gameweeks

def update_team_stats(league, only_newest):
    teams = datascraper.get_latest_stats(league, '2023')
    response = update_all_teams(league, teams)
    print(response)

def update_gameweeks(league, season):
    gameweeks = datascraper.get_all_gameweeks(league, season)
    response = update_all_gameweeks(league, '2023', gameweeks)
    print(response)

update_gameweeks('epl', '2023')