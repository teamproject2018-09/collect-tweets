#!/usr/bin/env python3
"""
    process-json.py: convert json file with tweets to csv format 
    usage: process-json.py infile1.json [infile2.json ...] > outfile.csv
    note: keeps only a selected group of fields of the json file
          (see FIELDNAMES variable for list)
    20180924 erikt(at)xs4all.nl
"""

import csv
from datetime import datetime
import json
import re
import sys

COMMAND = sys.argv.pop(0)
DATEFORMAT = "%a %b %d %H:%M:%S %z %Y"
FIELDNAMES = ["id","date","time","datetime","user","hashtags","mentions","reply-count","retweet-count","favorites-count","lang","text"]

patternNewline = re.compile(r"\n")
patternTimezone = re.compile(r" .\d\d\d\d ")
outFile = csv.DictWriter(sys.stdout,fieldnames=FIELDNAMES)
outFile.writeheader()
seen = {}
for inFileName in sys.argv:
    try: inFile = open(inFileName,"r")
    except: sys.exit(COMMAND+": cannot read file "+inFileName)
    for line in inFile:
        jsonLine = json.loads(line)
        if "full_text" in jsonLine and "id_str" in jsonLine and \
           "user" in jsonLine and "screen_name" in jsonLine["user"]:
            tweetId = jsonLine["id_str"]
            date = jsonLine["created_at"]
            date = datetime.strptime(jsonLine["created_at"],DATEFORMAT)
            timeString = date.strftime("%H:%M:%S")
            date = date.strftime("%Y-%m-%d")
            datetimeString = date+"T"+timeString+"+00:00"
            screenName = jsonLine["user"]["screen_name"]
            text = jsonLine["full_text"]
            text = patternNewline.sub(" ",text)
            replyCount = "0" # unavailable in json
            retweetCount = jsonLine["retweet_count"]
            favoritesCount = jsonLine["favorite_count"]
            hashtagList = [e["text"] for e in jsonLine["entities"]["hashtags"]]
            hashtags = " ".join(hashtagList)
            mentionList = [e["screen_name"] for e in jsonLine["entities"]["user_mentions"]]
            mentions = " ".join(mentionList)
            lang = jsonLine["lang"]
            outFile.writerow({"id":tweetId,"date":date,"time":timeString,"datetime":datetimeString,"user":screenName,"hashtags":hashtags,"mentions":mentions,"reply-count":replyCount,"retweet-count":retweetCount,"favorites-count":favoritesCount,"lang":lang,"text":text})
    inFile.close()
