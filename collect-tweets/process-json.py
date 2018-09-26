import csv
from datetime import datetime
import json
import re
import sys

COMMAND = sys.argv[0]
DATEFORMAT = "%a %b %d %H:%M:%S %z %Y"
FIELDNAMES = ["id","date","time","datetime","user","hashtags","mentions","reply-count","retweet-count","favorites-count","text"]

patternNewline = re.compile(r"\n")
patternTimezone = re.compile(r" .\d\d\d\d ")
with sys.stdout as csvfile:
    outFile = csv.DictWriter(csvfile,fieldnames=FIELDNAMES)
    outFile.writeheader()
    for line in sys.stdin:
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
            outFile.writerow({"id":tweetId,"date":date,"time":timeString,"datetime":datetimeString,"user":screenName,"hashtags":hashtags,"mentions":mentions,"reply-count":replyCount,"retweet-count":retweetCount,"favorites-count":favoritesCount,"text":text})
    csvfile.close()
