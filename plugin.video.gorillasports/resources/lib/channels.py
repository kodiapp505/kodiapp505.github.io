from ast import IsNot
from email.header import make_header
import json
import math
import sys
import time
from urllib.parse import urlencode
import xbmcgui
import xbmcplugin
import xbmc
import xbmcaddon

from resources.lib import api

# Get the plugin url in plugin:// notation.
_URL = sys.argv[0]

# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])

_MEDIAPATH = xbmcaddon.Addon(id='plugin.video.gorillasports').getAddonInfo('path') + 'resources\\media\\'


def get_url(**kwargs):
    return '{}?{}'.format(_URL, urlencode(kwargs))


def list_sports():
    categories = api.get_sports()

    listing = []
    for category in categories:
        sport_name = category['sport_name']
        status_icon = category['status_icon']

        list_item = xbmcgui.ListItem(label=sport_name)
        list_item.setArt({'fanart': getFanart(sport_name), 'poster': getPoster(sport_name), 'icon': getStreamStatus(status_icon)})
        list_item.setInfo('video', {'title': sport_name})
        
        if category['league_name'] is None:
            url = '{0}?action=listleagues&sport={1}'.format(_URL, sport_name)
        else:
            url = '{0}?action=listcompetitions&sport={1}&league={2}'.format(_URL, sport_name, category['league_name'])

        listing.append((url, list_item, True))
    
    xbmcplugin.addDirectoryItems(_HANDLE, listing, len(listing))
    xbmcplugin.endOfDirectory(_HANDLE)



def list_leagues(sport):
    leagues = api.get_leagues(sport)

    listing = []
    for league in leagues:
        status_icon = league['status_icon']

        list_item = xbmcgui.ListItem(label=league['league_name'])
        list_item.setArt({'poster': getPoster(sport), 'icon': getStreamStatus(status_icon), 'fanart': getFanart("_")})
        list_item.setInfo('video', {'title': league['league_name']})
        
        url = '{0}?action=listcompetitions&sport={1}&league={2}'.format(_URL, league['sport_name'], league['league_name'])
        listing.append((url, list_item, True))

    xbmcplugin.addDirectoryItems(_HANDLE, listing, len(listing))
    xbmcplugin.endOfDirectory(_HANDLE)



def list_competitions(sport, league):
    matches = api.get_competitions(sport, league)
    listing = []
    for match in matches:
        status_icon = match['status_icon']

        if len(match['competitors']) == 0:
            continue

        visitor = match['competitors'][0]
        home = match['competitors'][1]

        if visitor['name'] is None or visitor['name'] == "":
            match_title = home['name']
            match_title_noscore = home['name']
        else:
            hScore = " [COLOR orange]" + home['score'] + "[/COLOR]"
            vScore = " [COLOR orange]" + visitor['score'] + "[/COLOR]"
            match_title = visitor['name'] + vScore + "[LIGHT][I] vs [/I] [/LIGHT]" + home['name'] + hScore
            match_title_noscore = visitor['name'] + " vs " + home['name']

        if match['status_description'] is None or match['status_description'] == "":
            status_description = ""
        else:
            status_description = "[I]" + match['status_description'] + " - [/I] "

        if match['status'] == 'finished':
            title = "[COLOR darkred]"  + match_title  + "[/COLOR]"
        elif match['status'] == 'notstarted':
            title = "[I]" + time.strftime('(%m/%d %I:%M%p)', time.localtime(match['start_utc_timestamp'])) + "[/I] [B][COLOR lightgray]  " + match_title_noscore + "[/COLOR][/B]"
        else:
            title =  status_description + "[B]" + match_title + "[/B]"

        list_item = xbmcgui.ListItem(label=title)
        list_item.setArt({'poster': getCompetitionPoster(match['poster']), 'icon': getStreamStatus(status_icon), 'fanart': getFanart("_")})
        list_item.setInfo('video', {'title': match_title})
        url = '{0}?action=liststreams&sport={1}&id={2}'.format(_URL, match["sport_id"], match['id'])
        listing.append((url, list_item, True))
    
    xbmcplugin.addDirectoryItems(_HANDLE, listing, len(listing))
    xbmcplugin.endOfDirectory(_HANDLE)


def list_streams(sport, eventId):
    xbmcplugin.setContent(_HANDLE, 'videos')
    streams = api.get_streams(sport, eventId)
    listing = []

    for stream in streams:
        title = stream['name'] + " - " + stream['quality'] + " - [" + stream['language'] + "]"
        if stream['stream_online'] == True:
            title = "[B][COLOR green]" + title + "[/COLOR][/B]"

        list_item = xbmcgui.ListItem(label=title)
        list_item.setInfo('video', {'title': title})
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='play', url=stream['stream_url'])
        listing.append((url, list_item, False))
    
    xbmcplugin.addDirectoryItems(_HANDLE, listing, len(listing))
    xbmcplugin.endOfDirectory(_HANDLE)



def play_video(streamUrl):
    xbmc.log(streamUrl, xbmc.LOGINFO)
    
    play_item = xbmcgui.ListItem(path=streamUrl)
    #play_item.setMimeType('application/xml+dash')
    #play_item.setContentLookup(False)
    #play_item.setProperty('inputstream', 'inputstream.adaptive')
    #play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
    ####play_item.setProperty('inputstream.adaptive.stream_headers', 'User-Agent=the_user_agent&Cookie=the_cookies')

    xbmcplugin.setResolvedUrl(_HANDLE, True, listitem=play_item)



def getPoster(sport_name):
    return _MEDIAPATH + '\\posters\\sports\\' + sport_name + ".png"

def getFanart(sport_name):
    return _MEDIAPATH + '\\fanart\\sports\\' + sport_name + ".jpg"

def getStreamStatus(stream_status):
    return _MEDIAPATH + '\\icons\\status-' + stream_status + ".png"

def getCompetitionPoster(poster):
    if poster.lower().startswith("http"):
        return poster
    else:
        return _MEDIAPATH + poster
  
       