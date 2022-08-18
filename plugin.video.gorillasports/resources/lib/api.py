import imp
import time
import requests
from bs4 import BeautifulSoup
import simplejson as json

import xbmc

#_APIBASE = "http://mossgreen69-001-site1.ftempurl.com/api"
_APIBASE = "http://kodi701.somee.com/api"


def get_sports():
    try:
        r = requests.get(_APIBASE + "/sports")
        return json.loads(r.text)
    except:
        return []

def get_leagues(sport):
    try:
        r = requests.get(_APIBASE + "/leagues?sport_name=" + sport)
        return json.loads(r.text)
    except:
        return []

def get_competitions(sport, league):
    try:
        r = requests.get(_APIBASE + "/competitions?sport_name=" + sport + "&league_name=" + league)
        return json.loads(r.text)
    except:
        return []

def get_streams(sport, event):
    try:
        r = requests.get(_APIBASE + "/streams?sport_id=" + sport + "&match_id=" + event)
        return json.loads(r.text)
    except:
        return []
