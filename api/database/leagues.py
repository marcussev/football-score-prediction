from .db import db

collection = db.collection('leagues')

def get_all_teams(league):
    docs = collection.document(league).collection('teams').stream()
    teams = {}
    for doc in docs:
        teams[doc.id] = doc.to_dict()
    return teams

def get_team(league, team):
    doc = collection.document(league).collection('teams').document(team).get()
    return doc.to_dict()

## TODO: fetch list of all seasons for league
def get_all_seasons(league):
    return

## TODO: fetch all round data for given season
def get_season(league, season):
    return

## TODO: fetch list of all gameweeks for league and season
def get_all_gameweeks(league, season):
    return

## TODO: fetch all games from given gameweek of given league and season
def get_gameweek(league, season, gw):
    return

## TODO: fetch given game
def get_game(league, season, gw, match_id):
    return

# Update all team stats
def update_all_teams(league, teams):
    batch = db.batch()

    teams_col_ref = collection.document(league).collection('teams')
    for team in teams:
        data = teams[team]
        batch.set(teams_col_ref.document(team), data)

    res = batch.commit()
    return res

# Update data for all gameweeks of season
def update_all_gameweeks(league, season, gameweeks):
    batch = db.batch()

    gw_col_ref = collection.document(league).collection('seasons').document(season).collection('gameweeks')
    for gw in gameweeks:
        data = gameweeks[gw]
        for game in data:
            game_data = data[game]
            batch.set(gw_col_ref.document(str(gw)).collection('matches').document(game_data['title']), game_data)

    res = batch.commit()
    return res

# Update data for single gameweek of season
def update_gameweek(league, season, gw):
    return
