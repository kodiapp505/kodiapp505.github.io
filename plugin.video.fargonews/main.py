import sys
from urllib.parse import parse_qsl
import xbmc
from resources.lib import livestream, channels, vuit

#xbmc.log(vuit.get_mainpage(), xbmc.LOGINFO)
#xbmc.log(vuit.get_streams(), xbmc.LOGINFO)

# Get the plugin url in plugin:// notation.
_URL = sys.argv[0]
# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])



def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            channels.list_videos(params['key'])
        elif params['action'] == 'play':
            src = params['src']

            if params['resolver'] == 'livestream':
                src = livestream.resolveSrc(src)
            
            if params['resolver'] == 'vuit':
                src = vuit.resolveVodUrl(src)
            
            channels.play_video(src)
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        channels.list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
