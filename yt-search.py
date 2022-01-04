import urllib.request, re, random, string

# Collect random word from the configured word site.
# Get list of words from site, choose one randomly, and return single word as string
def randomWord():
    wordSite = "https://www.mit.edu/~ecprice/wordlist.100000"
    wordString = urllib.request.urlopen(wordSite).read().decode()
    wordList = str(wordString).splitlines()
    finalWord = wordList[random.randint(0, len(wordList)-1)]
    return(finalWord)

#searches for search term and returns a list of video IDs
def findVideos(searchTerm):
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+str(searchTerm)+"&sp=CAI%253D")
    videoIds = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return(videoIds)

print(findVideos(randomWord()))