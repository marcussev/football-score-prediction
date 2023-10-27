from .db import db

collection = db.collection('leagues')

def get_all_leagues():
    docs = collection.stream()
    leagues = {}
    for doc in docs:
        leagues[doc.id] = doc.to_dict()
    return leagues

def get_league(league):
    doc = collection.document(league).get()
    return doc.to_dict()

def get_all_teams(league):
    docs = collection.document(league).collection('teams').stream()
    teams = {}
    for doc in docs:
        teams[doc.id] = doc.to_dict()
    return teams

def get_team(league, team):
    doc = collection.document(league).collection('teams').document(team).get()
    return doc.to_dict()

def get_all_seasons(league):
    docs = collection.document(league).collection('seasons').stream()
    seasons = {}
    for doc in docs:
        seasons[doc.id] = doc.to_dict()
    return seasons

def get_season(league, season):
    doc = collection.document(league).collection('seasons').document(season).get()
    return doc.to_dict()

def get_all_gameweeks(league, season):
    docs = collection.document(league).collection('seasons').document(season).collection('gameweeks').stream()
    gameweeks = {}
    for doc in docs:
        gameweeks[doc.id] = doc.to_dict()
    return gameweeks

def get_gameweek(league, season, gw):
    doc = collection.document(league).collection('seasons').document(season).collection('gameweeks').document(gw).get()
    data = doc.to_dict()
    match_docs = collection.document(league).collection('seasons').document(season).collection('gameweeks').document(gw).collection('matches').stream()
    matches = {}
    for match_doc in match_docs:
        matches[match_doc.id] = match_doc.to_dict()
    data['matches'] = matches
    return data


def get_game(league, season, gw, match_id):
    doc = collection.document(league).collection('seasons').document(season).collection('gameweeks').document(gw).collection('matches').document(match_id).get()
    return doc.to_dict()

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
        batch.set(gw_col_ref.document(str(gw)), {'start_date': data['start_date'], 'end_date': data['end_date']}, merge=True)
        for game in data['matches']:
            game_data = data['matches'][game]
            batch.set(gw_col_ref.document(str(gw)).collection('matches').document(game_data['title']), game_data)

    res = batch.commit()
    return res

def update_gameweek(league, season, gw):
    return

def update_predictions(league, season, gw, predictions):
    batch = db.batch()

    matches_col_ref = collection.document(league).collection('seasons').document(season).collection('gameweeks').document(gw).collection('matches')
    for pred in predictions:
        batch.set(matches_col_ref.document(pred), {'A_predicted_score': predictions[pred][0], 'B_predicted_score': predictions[pred][1]}, merge=True)

    res = batch.commit()
    return res

