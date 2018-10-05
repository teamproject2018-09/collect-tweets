#!/usr/bin/env python3
"""
    process-html.py: convert html file with tweets to csv format 
    usage: process-html.py infile1.html [infile2.html ...] > outfile.csv
    note: keeps only a selected group of fields of the json file
          (see FIELDNAMES variable for list)
          html files were search results from the Twitter website saved in Firefox browser
    20180924 erikt(at)xs4all.nl
"""

from bs4 import BeautifulSoup
import csv
import re
import sys
import time

COMMAND = sys.argv.pop(0)
FIELDNAMES = ["id","date","time","datetime","user","hashtags","mentions","reply-count","retweet-count","favorites-count","lang","text"]

def getAttribute(tag,attrName):
    if attrName in tag.attrs: return(tag[attrName])
    else: return("")

def getText(tag,textTagName):
    for textTag in tag.find_all(textTagName): 
        if "lang" in textTag.attrs: lang = textTag["lang"]
        else: lang = ""
        return(textTag.text,lang)
    return("")

def getTimeDate(div):
    date,timeString,datetimeString = ["","",""]
    for span in div.find_all("span"):
        tmpDate = getAttribute(span,"data-time")
        if tmpDate != "":
            date = time.strftime("%Y-%m-%d",time.gmtime(int(tmpDate)))
            timeString = time.strftime("%H:%M:%S",time.gmtime(int(tmpDate)))
            datetimeString = date+"T"+timeString+"+00:00"
    return(date,timeString,datetimeString)

def getHashtags(div):
    hashtagList = []
    for a in div.find_all("a"):
        if "class" in a.attrs:
            for i in range(0,len(a["class"])):
                if a["class"][i] == "twitter-hashtag":
                    hashtag,lang = getText(a,"b")
                    hashtagList.append(hashtag)
    return(hashtagList)

def getCounts(div):
    retweetCount,favoritesCount,replyCount = ["0","0","0"]
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
    return(retweetCount,favoritesCount,replyCount)

patternNewline = re.compile(r"\n")
outFile = csv.DictWriter(sys.stdout,fieldnames=FIELDNAMES)
outFile.writeheader()
seen = {}
for inFileName in sys.argv:
    try: inFile = open(inFileName,"r")
    except: sys.exit(COMMAND+": cannot read file "+inFileName)
    html = BeautifulSoup(inFile,'html.parser')
    for div in html.find_all('div'):
        if "class" in div.attrs:
            for i in range(0,len(div["class"])):
                if div['class'][i] == "tweet":
                    tweetId = getAttribute(div,"data-tweet-id")
                    if not tweetId in seen:
                        seen[tweetId] = True
                        screenName = getAttribute(div,"data-screen-name")
                        mentions= getAttribute(div,"data-mentions")
                        date,timeString,datetimeString = getTimeDate(div)
                        retweetCount,favoritesCount,replyCount = getCounts(div)
                        text,lang = getText(div,"p")
                        text = patternNewline.sub(" ",text)
                        hashtagList = getHashtags(div)
                        hashtags = " ".join(hashtagList)
                        outFile.writerow({"id":tweetId,"date":date,"time":timeString,"datetime":datetimeString,"user":screenName,"hashtags":hashtags,"mentions":mentions,"reply-count":replyCount,"retweet-count":retweetCount,"favorites-count":favoritesCount,"lang":lang,"text":text})
    inFile.close()

