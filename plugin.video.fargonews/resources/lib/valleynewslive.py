from io import StringIO
import requests, gzip, time
from bs4 import BeautifulSoup
import simplejson as json
import xbmc
import random
from datetime import datetime, timezone
import time

def get_vods():
    # Get a basic token
    tokenHtml = requests.get("https://www.valleynewslive.com/pf/api/v3/content/fetch/syncbak-get-tokens", verify=False).text
    tokenJson = json.loads(tokenHtml)

    # Get a list of the available vods
    vodsHtml = requests.post("https://graphql-api.aws.syncbak.com/graphql", data=tokenJson['query'], headers={
        "content-type": "application/json; charset=utf-8",
        "api-token": tokenJson['apiToken'],
        "query-signature-token": tokenJson['querySignatureToken']
    }, verify=False).text
    vodsJson = json.loads(vodsHtml)['data']['videoOnDemand']
   
    result = []
    for vod in vodsJson:
        result.append({
            'name': "  [I]" + vod['title'] + "[/I]",
            'thumb': vod['listImages'][1]['url'],
            'src': vod['id'],
            'description': vod['description'],
            'resolver': 'valleynewslive'
        })
        
    return result

def resolveVodUrl(vodId):
    # get a token that has permission to play videos
    deviceId = getRandomSyncbackDeviceId()
    tokenHtml = requests.get("https://www.valleynewslive.com/pf/api/v3/content/fetch/syncbak-get-tokens?query=%7B%22deviceId%22:%22" + deviceId +"%22,%22queryString%22:%22%7B%5C%22query%5C%22:%5C%22query+GrayWebAppsVodItemData($vodId:+ID!,+$vodCount:+Int)%7B+videoOnDemandItem+(id:+$vodId)%7B+id+title+description+duration+airDate+listImages+%7B+type+url+size+%7D+posterImages+%7B+type+url+size+%7D+streamUrl+%7D+liveChannels+%7B+id+title+description+callsign+listImages+%7B+type+url+size+%7D+posterImages+%7B+type+url+size+%7D+isNew+type+status+onNow+%7B+id+title+description+episodeTitle+tvRating+startTime+endTime+duration+isLooped+isOffAir+airDate%7D+onNext+%7B+id+title+description+episodeTitle+tvRating+startTime+endTime+duration+isLooped+isOffAir+airDate%7D+isNielsenEnabled+isClosedCaptionEnabled+location+networkAffiliation+taxonomy+%7B+facet+terms+%7D+%7D+videoOnDemand+(first:+$vodCount)%7B+id+title+description+duration+airDate+listImages+%7B+type+url+size+%7D+posterImages+%7B+type+url+size+%7D+%7D+%7D%5C%22,%5C%22variables%5C%22:%7B%5C%22vodCount%5C%22:25,%5C%22vodId%5C%22:%5C%22" + vodId + "%5C%22%7D%7D%22%7D&_website=kvly", verify=False).text
    tokenJson = json.loads(tokenHtml)
    
    # query for the specific vod stream url
    vodsHtml = requests.post("https://graphql-api.aws.syncbak.com/graphql", data=tokenJson['query'], headers={
        "content-type": "application/json; charset=utf-8",
        "api-token": tokenJson['apiToken'],
        "query-signature-token": tokenJson['querySignatureToken']
    }, verify=False).text

    return json.loads(vodsHtml)['data']['videoOnDemandItem']['streamUrl']


# The API service uses a random token to help identify users.
def getRandomSyncbackDeviceId():
    chars = "useandom-26T198340PX75pxJACKVERYMINDBUSHWOLF_GQZbfghjklqvwyzrict"
    result = ''.join(random.choice(chars) for _ in range(50))
    return result

def formatDateToCentral(utcDateString):
    utc_time = datetime.strptime(utcDateString, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc_time = utc_time.replace(tzinfo=timezone.utc)
    local_time = utc_time.astimezone(None)
    formatted_time = local_time.strftime('%A %B %d, %Y')
    return formatted_time