from flask import Blueprint, request, jsonify
import pandas as pd
import json
import sys
import os

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



