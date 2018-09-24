import json
import sys

HASHTAGS = "hashtags"
MENTIONS = "user_mentions"

def extractFromList(thisList,key):
    outDict = {}
    for listDict in thisList: outDict[listDict[key]] = True
    return(outDict)

def addToDict(inList,outList):
    for key in inList:
        if not key in outList: outList[key] = 0
        outList[key] += 1

hashtags = {}
mentions = {}
for line in sys.stdin:
    myDict = eval(line)
    hashtagsNew = extractFromList(myDict["entities"][HASHTAGS],"text")
    addToDict(hashtagsNew,hashtags)
    mentionsNew = extractFromList(myDict["entities"][MENTIONS],"screen_name")
    addToDict(mentionsNew,mentions)

for hashtag in hashtags: print(hashtags[hashtag],"HASHTAG",hashtag)
for mention in mentions: print(mentions[mention],"MENTION",mention)

