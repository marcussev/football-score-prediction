from .db import db

collection = db.collection('leagues')

# Update all team stats
def update_all_teams(league, teams):
    batch = db.batch()

    teams_col_ref = collection.document(league).collection('teams')
    for team in teams:
        data = teams[team]
        batch.set(teams_col_ref.document(team), data)

    res = batch.commit()
    return res