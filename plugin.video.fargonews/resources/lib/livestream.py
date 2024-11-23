import requests
from bs4 import BeautifulSoup
import simplejson as json

def resolveSrc(playerUrl):
    try:
        r = requests.get(playerUrl)
        s = BeautifulSoup(r.text, 'html.parser')
        scripts = s.find_all('script')
        payload = scripts[0].string.replace("window.config = ", "")[:-1]
        streamInfo = json.loads(payload)['event']['stream_info']
        m3u8Url = streamInfo['m3u8_url']
        return m3u8Url
    except:
        return


def getDuluthHarborUrl():
    return "https://livestream.com/accounts/27442514/events/8331544/player"
