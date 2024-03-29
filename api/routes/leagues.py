from flask import Blueprint, jsonify, request
from jobs import update_gameweeks, update_team_stats, update_predictions

import db

leagues_blueprint = Blueprint('api/leagues', __name__)

@leagues_blueprint.route('/all', methods=['GET'])
def get_all_leagues():
    try:
        res = db.get_all_leagues()
        return jsonify(res), 200
    except:
        return 'Error: Could not retrieve all leagues', 400

@leagues_blueprint.route('/<league_id>', methods=['GET'])
def get_league(league_id):
    try:
        res = db.get_league(league_id)
        return jsonify(res), 200
    except:
        return 'Error: Could not retrieve league', 400

@leagues_blueprint.route('/<league_id>/teams/all', methods=['GET'])
def get_league_teams(league_id):
    try:
        res = db.get_all_teams(league_id)
        return jsonify(res), 200
    except:
        return 'Error: Could not retrieve all teams', 400

@leagues_blueprint.route('/<league_id>/teams/<team_id>', methods=['GET'])
def get_team(league_id, team_id):
    try:
        res = db.get_team(league_id, team_id)
        return jsonify(res), 200
    except:
        return 'Error: Could not retrieve team', 400

@leagues_blueprint.route('/<league_id>/seasons/all', methods=['GET'])
def get_all_seasons(league_id):
    try:
        res = db.get_all_seasons(league_id)
        return jsonify(res), 200
    except:
        return 'Error: Could not retrieve all seasons', 400

@leagues_blueprint.route('/<league_id>/seasons/<season_id>', methods=['GET'])
def get_season(league_id, season_id):
    try:
        res = db.get_season(league_id, season_id)
        return jsonify(res), 200
    except:
        return 'Error: Could not retrieve season', 400

@leagues_blueprint.route('/<league_id>/seasons/<season_id>/gameweeks/all', methods=['GET'])
def get_all_gameweeks(league_id, season_id):
    try:
        res = db.get_all_gameweeks(league_id, season_id)
        return jsonify(res), 200
    except:
        return 'Error: Could not retrieve all gameweeks', 400

@leagues_blueprint.route('/<league_id>/seasons/<season_id>/gameweeks/<gameweek_id>', methods=['GET'])
def get_gameweek(league_id, season_id, gameweek_id):
    try:
        res = db.get_gameweek(league_id, season_id, gameweek_id)
        return jsonify(res), 200
    except:
        return 'Error: Could not retrieve gameweek', 400
    
@leagues_blueprint.route('/<league_id>/seasons/<season_id>/gameweeks/<gameweek_id>/match/<match_id>', methods=['GET'])
def get_match(league_id, season_id, gameweek_id, match_id):
    try:
        res = db.get_match(league_id, season_id, gameweek_id, match_id)
        return jsonify(res), 200
    except:
        return 'Error: Could not retrieve match', 400
    
@leagues_blueprint.route('/<league_id>/seasons/<season_id>/scrape', methods=['POST'])
def scrape_season(league_id, season_id):
    try:
        res = update_gameweeks(league_id, season_id)
        return jsonify(res), 200
    except:
        return 'Error: Could not scrape season', 400
    
@leagues_blueprint.route('/<league_id>/teams/scrape', methods=['POST'])
def scrape_teams(league_id):
    try:
        res = update_team_stats(league_id)
        return jsonify(res), 200
    except:
        return 'Error: Could not scrape teams', 400
    
@leagues_blueprint.route('/<league_id>/seasons/<season_id>/gameweeks/<gameweek_id>/predict', methods=['POST'])
def predict_gameweek(league_id, season_id, gameweek_id):
    try:
        res = update_predictions(league_id, season_id, gameweek_id)
        return jsonify(res), 200
    except:
        return 'Error: Could not scrape predictions', 400