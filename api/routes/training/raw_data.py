from flask import Blueprint, request, jsonify
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import json
from understat import Understat

import db

raw_blueprint = Blueprint('api/training/data', __name__)

# Fetches entire list of raw data
@raw_blueprint.route('/all', methods=['GET'])
def get_all():
    res = db.get_all_raw_data()
    return jsonify(res), 200

# Insert an array of new entries to raw data
@raw_blueprint.route('/insert', methods=['POST'])
def insert_data():
    raw_data = request.data.games

    try:
        db.insert_raw_data(raw_data)
    except ValueError:
        return 'Insertion of raw data failed', 500
    
    return 'OK', 200

# Insert raw data from local file
@raw_blueprint.route('/insert_from_file', methods=['POST'])
def insert_data_from_file():
    dir_path = os.path.dirname(__file__)
    file_name = os.path.join(dir_path, '../../../data/datasets/interim/game_stats.csv').replace('\\', '/')
    raw_data = pd.read_csv(file_name).to_dict('records')

    try:
        db.insert_raw_data(raw_data)
    except ValueError:
        return 'Insertion of raw data failed', 500
    
    return 'OK', 200

@raw_blueprint.route('/scrape', methods=['GET', 'POST'])
def refresh_data():
    season = request.args.get('season')
    team = request.args.get('team')

    base_url = 'https://understat.com/team/'
    url = base_url + team + '/' + season

    print(season)
    print(team)

    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    scripts = soup.find_all('script')
    strings = scripts[1].string
    
    ind_start = strings.index("('")+2 
    ind_end = strings.index("')") 
    json_data = strings[ind_start:ind_end] 
    json_data = json_data.encode('utf8').decode('unicode_escape')

    # All teams matches for the season
    data = json.loads(json_data)

    return 'OK', 200
