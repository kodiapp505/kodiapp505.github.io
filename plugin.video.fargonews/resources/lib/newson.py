import time
import requests
from bs4 import BeautifulSoup
import simplejson as json

def get_clips():
    try:
        r = requests.get("https://newson.us/stationDetails/161")
        s = BeautifulSoup(r.text, 'html.parser')
        payload = s.find_all(id='__NEXT_DATA__')[0].string
        stationContent = json.loads(payload)['props']['pageProps']['data']['stationItemsContent']
        
        baseUri = stationContent['latest']['streamUrl'] 
        clips = []
        clips.append(stationContent['latest'])
        clips.extend(stationContent['programs'])

        result = []
        result.append({
            'name': "[B][COLOR blue]WDAY Live[/COLOR][/B]",
            'thumb': 'https://cdn.forumcomm.com/dims4/default/97a46a6/2147483647/strip/true/crop/3240x2160+300+0/resize/840x560!/quality/90/?url=https%3A%2F%2Fforum-communications-production-web.s3.amazonaws.com%2Fbrightspot%2Fbc%2F48%2F43b3ec9f4a4b812e418654979f72%2Fwday-splash-screen.jpg',
            'src': baseUri[:baseUri.find("?")] + "?a=b",
            'description': "Live Stream",
            'resolver': 'newson'
        })
        for c in clips:
            if c['name'].find('Agweek') >= 0:
                continue

            result.append({
                'name': "  [I]" + c['name'] + " - " + time.strftime('%A %B %d, %Y', time.localtime(c['startTime'])) + "[/I]",
                'thumb': 'https://cdn.forumcomm.com/dims4/default/97a46a6/2147483647/strip/true/crop/3240x2160+300+0/resize/840x560!/quality/90/?url=https%3A%2F%2Fforum-communications-production-web.s3.amazonaws.com%2Fbrightspot%2Fbc%2F48%2F43b3ec9f4a4b812e418654979f72%2Fwday-splash-screen.jpg',
                'src': c['streamUrl'],
                'description': c['description'],
                'resolver': 'newson'
            })

        return result
    except:
        return []

def resolveSrc(src):
    return src
