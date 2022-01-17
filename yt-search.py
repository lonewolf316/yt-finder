import urllib.request, re, random, string
from googleapiclient.discovery import build

#Set up initial API settings and return youtube object to pass to later functions
def youtubeSetup(DEVELOPER_KEY):
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    return(youtube)

# Collect random word from the configured word site
# Get list of words from site, choose one randomly, and return single word as string
def randomWord():
    wordSite = "https://www.mit.edu/~ecprice/wordlist.100000"
    wordString = urllib.request.urlopen(wordSite).read().decode()
    wordList = str(wordString).splitlines()
    finalWord = wordList[random.randint(0, len(wordList)-1)]
    return(finalWord)

#performs search with basic youtube filter parameters and returns a list of video IDs 
def youtubeSearch(youtube, searchTerm):
    searchResponse = youtube.search().list(q=searchTerm, part='snippet', order='date', type='video', videoDuration='short', maxResults=50).execute()
    allIds = []
    for item in searchResponse.get('items', []):
        allIds.append(item['id']['videoId'])
    print("Number of videos found: "+str(len(allIds)))
    return(allIds)

#Intakes the list of IDs and gathers more stats on the video and sorts with more specific parameters ex: length and view count
def parseVideoData(youtube, videoIdList, maxView=200, minView=0):
    matchingIds = []
    for videoId in videoIdList:
        statsResponse = youtube.videos().list(part='statistics, contentDetails', id=videoId).execute()
        vidDuration = statsResponse.get('items', [])[0]['contentDetails']['duration']
        vidViews = int(statsResponse.get('items', [])[0]['statistics']['viewCount'])
        if vidViews < maxView and vidViews > minView:
            matchingIds.append(videoId)
    return(matchingIds)

#Converts a list of IDs to Youtube links
def idToLink(idList):
    linkList = []
    for id in idList:
        url="https://www.youtube.com/watch?v="+str(id)
        linkList.append(url)
    return(linkList)

if __name__ == "__main__":
    import keys
    DEVELOPER_KEY = keys.YOUTUBE_KEY
    youtube = youtubeSetup(DEVELOPER_KEY) #create youtube api object
    searchWord = randomWord() #generate a random word to search for - just returns a string
    searchResults = youtubeSearch(youtube, searchWord) #pass youtube object and string into function to conduct a search. returns a list of <=50 results
    matchingResults = parseVideoData(youtube, searchResults) #results are parsed and checked for time and view count to match settings. returns list of video IDs
    linkList = idToLink(matchingResults) #video ID list is converted to list of links for ease of use.
    print(linkList)