from io import StringIO
import requests, gzip, time
from bs4 import BeautifulSoup
import simplejson as json

def get_vods():
    content = __request("https://www.vuit.com/publishers/235/kvly-my-newsfeed")
    s = BeautifulSoup(content, 'html.parser')
    payload = s.find_all("script", attrs={"type": "text/javascript"})[2].string

    startIndex = payload.find("var json={") + 9
    endIndex = payload.find("$(document).data(")

    jsonStr = str(payload)[startIndex:endIndex].strip()[:-1]
    publisherGroups = json.loads(jsonStr)['publisher']['publisherGroups']

    stationId = None
    vodDict = {}
    for group in publisherGroups:
        if group['displayName'] == "Video on Demand":
            for vod in group["vods"][:10]:
                vodDict[vod['airDate']] = vod
        if group['displayName'] == "Clips":
            hlsUrl = group['clips'][0]['hlsUrl']
            startIdx = hlsUrl.find("/clips/") + 7
            endIdx = hlsUrl.find("/", startIdx)
            stationId = hlsUrl[startIdx:endIdx]

    
    result = []
    for vod in vodDict.values():
        result.append({
            'name': "  [I]" + vod['name'] + " - " + time.strftime('%A %B %d, %Y', time.localtime(vod['airDate'])) + "[/I]",
            'thumb': 'https://' + vod['images'][0]['url'] if len(vod['images']) > 0 else '',
            'src': "https://www.vuit.com/api/services/StreamInfo?stationId=" + str(vod['channelId']) + "&mediaId=" + str(vod['mediaId']),
            'description': vod['description'],
            'resolver': 'vuit'
        })
        
    return result

def get_live_stream():
    content = __request("https://www.valleynewslive.com/pf/api/v3/content/fetch/site-service?query=%7B%22section%22:%22%2Fvideo%22,%22websiteOverride%22:%22kvly%22%7D&_website=kvly")
    streamUrl = json.loads(content)['site']['syncbak_livestream_tokens']['livestream1']
    
    if streamUrl.startswith("//"):
        streamUrl = "https:" + streamUrl

    return [
        {
                'name': '[COLOR blue][B]KVLY News Live[/B][/COLOR]',
                'thumb': 'https://play-lh.googleusercontent.com/UwqV9DC0OwVDFNKOJBURdedMX22jtOJmErh8n4c6eZL6w4D_HJCv0_rFH9WO3a74hA',
                'resolver': 'newson',
                'src': streamUrl,
                'description': ''
            }
    ]

def get_latest_weather():
    content = __request("https://www.valleynewslive.com/pf/api/v3/content/fetch/wx-todays-forecast?query=%7B%22includeSections%22%3A%22%2Fweather%2Fforecast%22%7D&_website=kvly")    
    streamData = json.loads(content)['promo_items']['lead_art']
    return [
        {
                'name': '[COLOR green][B]Weather Highlight[/B][/COLOR]',
                'thumb': streamData['promo_image']['url'],
                'resolver': 'newson',
                'src': streamData['streams'][5]['url'],
                'description': ''
            }
    ] 



def get_streams():
    return __request("https://www.vuit.com/api/services/StreamInfo?stationId=20585")


def resolveVodUrl(streamInfoUrl):
    content = __request(streamInfoUrl)
    streamUrl = json.loads(content)['streamUrl']
    return streamUrl


def __request(url):
    r = requests.get(url)

    try:
        encoding = r.info().getheader('Content-Encoding')
    except:
        encoding = None

    if encoding == 'gzip':
        return gzip.GzipFile(fileobj=StringIO(r.text)).read()
    else:
        return r.text
    