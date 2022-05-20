import sys
from urllib.parse import urlencode
import xbmcgui
import xbmcplugin
import xbmc
import xbmcaddon

from resources.lib import newson, vuit

#Detroit Lakes
#https://livestream.com/accounts/27442514/events/8331548/player

#Forum Tower Cam Fargo
#https://livestream.com/accounts/27442514/events/8305238/player

#WDAY+
#https://livestream.com/accounts/27442514/events/8305246/player

# Get the plugin url in plugin:// notation.
_URL = sys.argv[0]

# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])

_MEDIAPATH = xbmcaddon.Addon(id='plugin.video.fargonews').getAddonInfo('path') + 'resources\\media\\'



def get_url(**kwargs):
    return '{}?{}'.format(_URL, urlencode(kwargs))

def get_categories():
    return [
        {
            "key": "WDAY",
            "name": "WDAY News",
            "icon": _MEDIAPATH + "wday.icon.png",
            "thumb": _MEDIAPATH + "wday.thumb.png",
            "description": "WDAY News"
        },
        {
            "key": "VNL",
            "name": "Valley News Live",
            "icon": _MEDIAPATH + "klvy.icon.png",
            "thumb": _MEDIAPATH + "klvy.thumb.png",
            "description": "Valley News Live"
        },
        {
            "key": "MSM",
            "name": "Network Media",
           "icon": _MEDIAPATH + "networks.icon.png",
            "thumb": _MEDIAPATH + "networks.thumb.png",
            "description": "FOX, CNN, ABC, MSNBC, ..."
        },
        {
            "key": "TC",
            "name": "Tower Cams",
            "icon": _MEDIAPATH + 'towercam.icon.png',
            "thumb": _MEDIAPATH + "towercam.thumb.png",
            "description": "Tower Cams"
        }
    ]

# Fox News
# 'https://trn03.tulix.tv/AsEAeOtIxz/playlist.m3u8',
def get_videos(key):
    if key == 'WDAY':
        streams = [
            {
                'name': '[COLOR blue][B]WDAY Storm Tracker[/B][/COLOR]',
                'thumb': 'https://play-lh.googleusercontent.com/UwqV9DC0OwVDFNKOJBURdedMX22jtOJmErh8n4c6eZL6w4D_HJCv0_rFH9WO3a74hA',
                'resolver': 'livestream',
                'src': 'https://livestream.com/accounts/27442514/events/8331542/player',
                'description': 'Live weather information from WDAY storm tracker team.'
            }
        ]
        streams.extend(newson.get_clips())
        return streams
    elif key == "VNL":
        streams = vuit.get_live_stream()
        streams.extend(vuit.get_latest_weather())
        streams.extend(vuit.get_vods())
        return streams
    elif key == "MSM":
        return [
            {
                'name': '[COLOR red]CNN Live[/COLOR]',
                'thumb': 'https://www.logodesignlove.com/wp-content/uploads/2010/06/cnn-logo-white-on-red.jpg',
                'resolver': 'newson',
                'src': 'https://turnerlive.warnermediacdn.com/hls/live/586495/cnngo/cnn_slate/VIDEO_0_3564000.m3u8',
                'description': 'CNN GO.'
            },
            {
                'name': '[COLOR red]FOX Live[/COLOR]',
                'thumb': 'https://www.researchamerica.org/sites/default/files/logo_library/media/768px-Fox_News_Channel_logo.svg.png',
                'resolver': 'newson',
                'src': 'https://fox-foxnewsnow-samsungus.amagi.tv/playlist720p.m3u8',
                'description': 'FOX.'
            },
            {
                'name': '[COLOR red]MSNBC Live[/COLOR]',
                'thumb': 'http://www.freeintertv.com/images/tv/msnbc_live.jpg',
                'resolver': 'newson',
                'src': 'https://1420543146.rsc.cdn77.org/Q3LsNSHe9G3pjI88NPNXqg==,1653031597/LS-ATL-54548-10/tracks-v1a1/mono.m3u8|origin=https://www.livenewsnow.com&referer=https://www.livenewsnow.com',
                'description': 'MSNBC.'
            },
            {
                'name': '[COLOR red]CNBC Live[/COLOR]',
                'thumb': 'http://www.freeintertv.com/images/tv/cnbc_live.jpg',
                'resolver': 'newson',
                'src': 'https://1143561436.rsc.cdn77.org/ePDqbWmS0JDN8hRBisOAYg==,1653022388/1143561436/tracks-v1a1/mono.m3u8',
                'description': 'CNBC.'
            },
            {
                'name': '[COLOR red]Bloomberg Live[/COLOR]',
                'thumb': 'https://talkingbiznews.com/wp-content/uploads/2015/09/Bloomberg-Live.png',
                'resolver': 'newson',
                'src': 'https://liveproduseast.akamaized.net/us/Channel-USTV-AWS-virginia-2/Source-USTV-10000-1-slxdlg-BP-HD-4-86X4McEAF4SL_live.m3u8',
                'description': 'Bloomberg.'
            }
        ]

    elif key == "TC":
        return [
            {
            'name': '[COLOR FFAA6C39]Fargo Tower Cam[/COLOR]',
            'thumb': _MEDIAPATH + "towercam.thumb.png",
            'resolver': 'livestream',
            'src': 'https://livestream.com/accounts/27442514/events/8305238/player',
            'description': 'Fargo downtown tower cam'
        },
        {
            'name': '[COLOR FFAA6C39]Wahpeton Tower Cam[/COLOR]',
            'thumb': 'https://growthzonesitesprod.azureedge.net/wp-content/uploads/sites/2282/2021/04/city-sign-1024x683.jpg',
            'resolver': 'livestream',
            'src': 'https://livestream.com/accounts/27442514/events/8677382/player',
            'description': 'Live WDAY tower cam for Wahpeton, ND.'
        },
        {
            'name': '[COLOR FFAA6C39]Duluth Harbor Cam[/COLOR]',
            'thumb': 'https://www.dot.state.mn.us/historicbridges/bridge/L6116/image1-reduced.jpg',
            'resolver': 'livestream',
            'src': 'https://livestream.com/accounts/27442514/events/8331544/player',
            'description': 'The Duluth Aerial Lift Bridge is a span-drive configuration movable lift bridge constructed in 1901-1905 and modified in 1929. It is located on Lake Avenue and spans the Duluth Ship Canal, which connects the city of Duluth with Minnesota Point. The bridge was designed by Thomas F. McGilvray and C.A.P. Turner, and constructed by the Modern Steel Structural Company. The original 1901-1905 aerial bridge had a gondola car suspended by an inverted steel tower from the underside of the truss. This truss remains extant as a structural member of the bridge. In 1929 the bridge was modified by adding an elevating roadway to replace the traversing platform, lengthening the steel towers, and incorporating new structural support within the confines of the old towers to carry the counterweight roadway. It is significant as a rare type of bridge engineering and as a resource in the Duluth Ship Canal Historic District.'
        },
        ]   
    else:
        return []

#Fox News
#https://trn03.tulix.tv/AsEAeOtIxz/playlist.m3u8
#https://1028107998.rsc.cdn77.org/ZPuVsGG7RDzpAqV0DPJjjg==,1647331494/ls-54548-2/index.m3u8|referer=https://www.livenewsworld.com/

#ABC
#https://abc.com/watch-live/abc-news
#https://content-ause1-ur-dtci1.uplynk.com/channel/3324f2467c414329b3b0cc5cd987b6be/g.m3u8


def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    :return: None
    """
    # Get video categories
    categories = get_categories()
    # Create a list for our items.
    listing = []
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category['name'])
        # Set a fanart image for the list item.
        # Here we use the same image as the thumbnail for simplicity's sake.
        
        list_item.setArt({'icon': category['icon'], 'poster': category['thumb'], 'fanart': _MEDIAPATH + "fargo2.png"})
        #list_item.setArt({'icon': category['icon'], 'thumb': category['thumb'], 'fanart': _MEDIAPATH + "fargo2.png"})
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': category['name']})
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.fargonews/?action=listing&category=Animals
        url = '{0}?action=listing&key={1}'.format(_URL, category['key'])
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the listing as a 3-element tuple.
        listing.append((url, list_item, is_folder))
    # Add our listing to Kodi.
    # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
    # instead of adding one by ove via addDirectoryItem.
    xbmcplugin.addDirectoryItems(_HANDLE, listing, len(listing))
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)


def list_videos(key):
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get the list of videos in the category.
    videos = get_videos(key)
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': video['name'],
                                    'plot': video['description'],
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.fargonews/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', src=video['src'], resolver=video['resolver'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_HANDLE, True, listitem=play_item)