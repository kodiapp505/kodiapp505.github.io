import time
import requests
from bs4 import BeautifulSoup
import simplejson as json
import re

def get_vods():
    htmlSource = requests.get("https://www.inforum.com/wdayplus/wday-newscast-replays", verify=False).text
    s = BeautifulSoup(htmlSource, 'html.parser')

    video_wrapper = s.find('div', class_='videoWrapper')
    script_tag = video_wrapper.find('script')
    script_src = script_tag['src']

    scriptHtml = requests.get(script_src, verify=False).text
    pattern = r'"playlist":\s*"([^"]+)"'
    match = re.search(pattern, scriptHtml)
    playlist_url = match.group(1)

    vodsHtml = requests.get("https:" + playlist_url, verify=False).text
    vodsJson = json.loads(vodsHtml)['playlist']

    result = []
    for vod in vodsJson:
        if vod['duration'] < 30:
            continue

        result.append({
            'name': "  [I]" + vod['title'] + "[/I]",
            'thumb': vod['image'],
            'src': vod['sources'][0]['file'],
            'description': vod['description'],
            'resolver': 'wday'
        })

    return result
    

def resolveSrc(src):
    return src
