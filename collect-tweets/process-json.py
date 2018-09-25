import csv
import json
import re
import sys

COMMAND = sys.argv[0]
FIELDNAMES = ["id","date","user","hashtags","mentions","text"]

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
            date = patternTimezone.sub(" ",date)
            screenName = jsonLine["user"]["screen_name"]
            text = jsonLine["full_text"]
            text = patternNewline.sub(" ",text)
            hashtagList = [e["text"] for e in jsonLine["entities"]["hashtags"]]
            hashtags = " ".join(hashtagList)
            mentionList = [e["screen_name"] for e in jsonLine["entities"]["user_mentions"]]
            mentions = " ".join(mentionList)
            outFile.writerow({"id":tweetId,"date":date,"user":screenName,"hashtags":hashtags,"mentions":mentions,"text":text})
    csvfile.close()
