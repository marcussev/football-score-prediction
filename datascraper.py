import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://understat.com/'

# Gets basic stats for all teams in league
def get_latest_stats(league, season):
    url = BASE_URL + 'league/' + league + '/' + season
    res = requests.get(url)

    # Scrape for data
    soup = BeautifulSoup(res.content, 'lxml')
    scripts = soup.find_all('script')
    string = scripts[2].string

    # parsed data to json
    ind_start = string.index("('")+2
    ind_end = string.index("')")
    json_data = string[ind_start:ind_end]
    json_data = json_data.encode('utf8').decode('unicode_escape')
    raw_data = json.loads(json_data)

    data = {}
    
    for team_id in raw_data:
        team = raw_data[team_id]
        team_total_stats = {
            'xG': 0,
            'xGA': 0,
            'pts': 0,
            'goals': 0,
            'conceded': 0,
            'deep': 0,
            'deep_allowed': 0,
            'ppda': 0,
            'ppda_allowed': 0,
        }

        # Search each teams match history and calucate stats
        gameweek = 1
        for match in team['history']:
            team_total_stats['goals'] += match['scored']
            team_total_stats['xG'] += match['xG']
            team_total_stats['xGA'] += match['xGA']
            team_total_stats['pts'] += match['pts']
            team_total_stats['conceded'] += match['missed']
            team_total_stats['deep'] += match['deep']
            team_total_stats['deep_allowed'] += match['deep_allowed']
            team_total_stats['ppda'] += (match['ppda']['att']/match['ppda']['def'])
            team_total_stats['ppda_allowed'] += (match['ppda_allowed']['att']/match['ppda_allowed']['def'])
            gameweek += 1

        team_avg_stats = {
            'xG': team_total_stats['xG']/gameweek,
            'xGA': team_total_stats['xGA']/gameweek,
            'ppg': team_total_stats['pts']/gameweek,
            'gpg': team_total_stats['goals']/gameweek,
            'cpg': team_total_stats['conceded']/gameweek,
            'deep': team_total_stats['deep']/gameweek,
            'deep_allowed': team_total_stats['deep_allowed']/gameweek,
            'ppda': team_total_stats['ppda']/gameweek,
            'ppda_allowed': team_total_stats['ppda_allowed']/gameweek
        }

        data[team['title']] = team_avg_stats

    return data

get_latest_stats('epl', '2023')