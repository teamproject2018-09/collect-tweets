from bs4 import BeautifulSoup
import csv
import re
import sys
import time

COMMAND = sys.argv.pop(0)
FIELDNAMES = ["id","date","user","hashtags","mentions","text"]

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
                    for span in div.find_all("span"): 
                        tmpDate = getAttribute(span,"data-time")
                        if tmpDate != "": 
                            date = time.asctime(time.gmtime(int(tmpDate)))
                    hashtagList = []
                    for a in div.find_all("a"):
                        if "class" in a.attrs:
                            for i in range(0,len(a["class"])):
                                if a["class"][i] == "twitter-hashtag":
                                    hashtagList.append(getText(a,"b"))
                    hashtags = " ".join(hashtagList)
                    outFile.writerow({"id":tweetId,"date":date,"user":screenName,"hashtags":hashtags,"mentions":mentions,"text":text})

