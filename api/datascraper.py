import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timedelta

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
    raw_data = parseSoupString(string)

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

def get_all_gameweeks(league, season):
    url = BASE_URL + 'league/' + league + '/' + season
    res = requests.get(url)

    # Scrape for gw data
    soup = BeautifulSoup(res.content, 'lxml')
    scripts = soup.find_all('script')
    string = scripts[1].string

    raw_data = parseSoupString(string)

    raw_data.sort(key=lambda g: datetime.strptime(g.get('datetime'), '%Y-%m-%d %H:%M:%S'))

    gameweeks = {}

    current_gw = 1
    current_gw_start = None
    current_gw_end = None
    for game in raw_data:
        game_data = {
            'id': game['id'],
            'isPlayed': game['isResult'],
            'home': game['h']['title'],
            'away': game['a']['title'],
            'datetime': game['datetime'],
            'title': game['h']['title'] + ' - ' + game['a']['title'],
            'short_title': game['h']['short_title'] + ' - ' + game['a']['short_title'],
            'h_scored': game['goals']['h'],
            'a_scored': game['goals']['a'],
            'h_xG': game['xG']['h'],
            'a_xG': game['xG']['a']
        }
        
        newGameweek = False
        game_date = datetime.strptime(game['datetime'], '%Y-%m-%d %H:%M:%S')
        if current_gw in gameweeks and current_gw_end < game_date:
            newGameweek = True
        
        if newGameweek:
            current_gw += 1

        if current_gw not in gameweeks:
            gameweeks[current_gw] = {}
            gameweeks[current_gw]['matches'] = {}
            current_gw_start = previousWeekDay(datetime.strptime(game['datetime'], '%Y-%m-%d %H:%M:%S'), 0).replace(hour=0, minute=0, second=0, microsecond=0)
            current_gw_end = nextWeekDay(current_gw_start, 6).replace(hour=23, minute=59, second=59)
            gameweeks[current_gw]['start_date'] = current_gw_start
            gameweeks[current_gw]['end_date'] = current_gw_end

        gameweeks[current_gw]['matches'][game_data['title']] = game_data

    return gameweeks



def parseSoupString(string):
    ind_start = string.index("('")+2
    ind_end = string.index("')")
    json_data = string[ind_start:ind_end]
    json_data = json_data.encode('utf8').decode('unicode_escape')
    raw_data = json.loads(json_data)
    return raw_data

def nextWeekDay(date, weekday):
    days_ahead = weekday - date.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return date + timedelta(days_ahead)

def previousWeekDay(date, weekday):
    days_ahead = date.weekday() - weekday
    if days_ahead < 0:
        days_ahead -= 7
    return date - timedelta(days_ahead)
