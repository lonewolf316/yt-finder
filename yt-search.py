import urllib.request, re, random, string
import keys
from googleapiclient.discovery import build


DEVELOPER_KEY = keys.YOUTUBE_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

# Collect random word from the configured word site.
# Get list of words from site, choose one randomly, and return single word as string
def randomWord():
    wordSite = "https://www.mit.edu/~ecprice/wordlist.100000"
    wordString = urllib.request.urlopen(wordSite).read().decode()
    wordList = str(wordString).splitlines()
    finalWord = wordList[random.randint(0, len(wordList)-1)]
    return(finalWord)

#performs search with basic youtube filter parameters and returns a list of video IDs 
def youtubeSearch(searchTerm):
    searchResponse = youtube.search().list(q=searchTerm, part='snippet', order='date', type='video', videoDuration='short', maxResults=50).execute()
    allIds = []
    for item in searchResponse.get('items', []):
        allIds.append(item['id']['videoId'])
    print("Number of videos found: "+str(len(allIds)))
    return(allIds)

#Intakes the list of IDs and gathers more stats on the video and sorts with more specific parameters ex: length and view count
def parseVideoData(videoIdList, maxView=200, minView=0):
    matchingIds = []
    for videoId in videoIdList:
        statsResponse = youtube.videos().list(part='statistics, contentDetails', id=videoId).execute()
        vidDuration = statsResponse.get('items', [])[0]['contentDetails']['duration']
        vidViews = int(statsResponse.get('items', [])[0]['statistics']['viewCount'])
        print(vidViews)
        if vidViews < maxView and vidViews > minView:
            matchingIds.append(videoId)
    return(matchingIds)



print(parseVideoData(youtubeSearch(randomWord())))