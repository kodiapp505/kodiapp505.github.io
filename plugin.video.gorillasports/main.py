# Module: main
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
"""
Example video plugin that is compatible with Kodi 19.x "Matrix" and above
"""
import sys
from urllib.parse import parse_qsl
import xbmc
from resources.lib import channels

#xbmc.log(vuit.get_mainpage(), xbmc.LOGINFO)
#xbmc.log(vuit.get_streams(), xbmc.LOGINFO)

# Get the plugin url in plugin:// notation.
_URL = sys.argv[0]
# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])



def router(paramstring):
    
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listleagues':
            channels.list_leagues(params['sport'])
        elif params['action'] == 'listcompetitions':
            channels.list_competitions(params['sport'], params['league'])
        elif params['action'] == 'liststreams':
            channels.list_streams(params['sport'], params['id'])
        elif params['action'] == 'play':
            channels.play_video(params['url'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of sport categories
        channels.list_sports()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
