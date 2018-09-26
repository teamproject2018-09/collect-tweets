from bs4 import BeautifulSoup
import csv
import re
import sys
import time

COMMAND = sys.argv.pop(0)
FIELDNAMES = ["id","date","time","datetime","user","hashtags","mentions","reply-count","retweet-count","favorites-count","text"]

def getAttribute(tag,attrName):
    if attrName in tag.attrs: return(tag[attrName])
    else: return("")

def getText(tag,textTagName):
    for textTag in tag.find_all(textTagName): return(textTag.text)
    return("")

patternNewline = re.compile(r"\n")
with sys.stdout as csvfile:
    outFile = csv.DictWriter(csvfile,fieldnames=FIELDNAMES)
    outFile.writeheader()
    html = BeautifulSoup(sys.stdin,'html.parser')
    for div in html.find_all('div'):
        if "class" in div.attrs:
            for i in range(0,len(div["class"])):
                if div['class'][i] == "tweet":
                    screenName = getAttribute(div,"data-screen-name")
                    tweetId = getAttribute(div,"data-tweet-id")
                    mentions= getAttribute(div,"data-mentions")
                    text = getText(div,"p")
                    text = patternNewline.sub(" ",text)
                    date = ""
                    timeString = ""
                    datetimeString = ""
                    for span in div.find_all("span"): 
                        tmpDate = getAttribute(span,"data-time")
                        if tmpDate != "": 
                            date = time.strftime("%Y-%m-%d",time.gmtime(int(tmpDate)))
                            timeString = time.strftime("%H:%M:%S",time.gmtime(int(tmpDate)))
                            datetimeString = date+"T"+timeString+"+00:00"
                    hashtagList = []
                    for a in div.find_all("a"):
                        if "class" in a.attrs:
                            for i in range(0,len(a["class"])):
                                if a["class"][i] == "twitter-hashtag":
                                    hashtagList.append(getText(a,"b"))
                    retweetCount = 0
                    favoritesCount = 0
                    replyCount = 0
                    for span1 in div.find_all("span"):
                        if "class" in span1.attrs:
                            for i in range(0,len(span1["class"])):
                                if span1["class"][i] == "ProfileTweet-action--retweet":
                                    for span2 in span1.find_all("span"):
                                        if "data-tweet-stat-count" in span2.attrs:
                                            retweetCount = span2["data-tweet-stat-count"]
                                if span1["class"][i] == "ProfileTweet-action--favorite":
                                    for span2 in span1.find_all("span"):
                                        if "data-tweet-stat-count" in span2.attrs:
                                            favoritesCount = span2["data-tweet-stat-count"]
                                if span1["class"][i] == "ProfileTweet-action--reply":
                                    for span2 in span1.find_all("span"):
                                        if "data-tweet-stat-count" in span2.attrs:
                                            replyCount = span2["data-tweet-stat-count"]
                    hashtags = " ".join(hashtagList)
                    outFile.writerow({"id":tweetId,"date":date,"time":timeString,"datetime":datetimeString,"user":screenName,"hashtags":hashtags,"mentions":mentions,"reply-count":replyCount,"retweet-count":retweetCount,"favorites-count":favoritesCount,"text":text})

