import definitions
import json
import sys
import tweepy

TASK = "getUserTweets" # getUserTweets or searchForTweets
COMMAND = sys.argv.pop(0)
NBROFTWEETS = 200

def authenticate():
    # source: https://tweepy.readthedocs.io/en/v3.6.0/
    auth = tweepy.OAuthHandler(definitions.consumer_key,
                               definitions.consumer_secret)
    auth.set_access_token(definitions.token,
                          definitions.token_secret)
    return(auth)

# 20180925 not used yet
def limit_handled(cursor):
    while True: 
        try: yield cursor.next()
        except tweepy.RateLimitError: time.sleep(15 * 60)

def convertListToJson(thisList):
    return([json.dumps(json_obj) for json_obj in thisList])

def getUserTweets(api,userName,count):
    tweetList = [status._json for status in tweepy.Cursor(api.user_timeline,
                                                          screen_name=userName,
                                                          count=count,
                                                          tweet_mode="extended").items()] 
    return(convertListToJson(tweetList))

def searchForTweets(api,query,count):
    tweetList = [status._json for status in tweepy.Cursor(api.search,
                                                          q=query,
                                                          count=count,
                                                          tweet_mode="extended").items()] 
    return(convertListToJson(tweetList))

def printList(thisList):
    for t in thisList: print(t)
    return()

if len(sys.argv) < 1: sys.exit("usage: "+COMMAND+" user")
user = sys.argv.pop(0)

auth = authenticate()
api = tweepy.API(auth)
tweets = []
if TASK == "getUserTweets": tweets = getUserTweets(api,user,NBROFTWEETS)
elif TASK == "searchForTweets": tweets = searchForTweets(api,user,NBROFTWEETS)
else: sys.exit(COMMAND+": unknown task!")
printList(tweets)

