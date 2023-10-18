import datascraper
from api.database.leagues import update_all_teams

def update_team_stats(league, only_newest):
    teams = datascraper.get_latest_stats(league, '2023')
    response = update_all_teams(league, teams)
    print(response)

update_team_stats('Bundesliga', False)