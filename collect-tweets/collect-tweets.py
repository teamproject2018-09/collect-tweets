#!/usr/bin/env python3
"""
    collect-tweets.py: collect tweets from Twitter API
    usage: collect-tweets.py [-u|-s] user-name
    notes: 
    . requires twitter access keys stored in file definitions.py (not supplied)
    . requires python library tweepy for retrieving tweets
    . outputs json: one tweet per line
    . maximum search window is the most recent 10 days (set by Twitter)
    20180924 erikt(at)xs4all.nl
"""

import definitions
import getopt
import json
import sys
import tweepy

TASK = "getUserTweets" # getUserTweets or searchForTweets
COMMAND = sys.argv.pop(0)
USAGE = "usage: "+COMMAND+" [-u|-s] user"
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

opts,args = getopt.getopt(sys.argv,"su")
if len(opts) != 1 or len(args) != 1: sys.exit(USAGE)
user = args[0]
if opts[0][0] == "-u": TASK = "getUserTweets"
elif opts[0][0] == "-s": TASK = "searchForTweets"
else: sys.exit(USAGE)

auth = authenticate()
api = tweepy.API(auth)
tweets = []
if TASK == "getUserTweets": tweets = getUserTweets(api,user,NBROFTWEETS)
elif TASK == "searchForTweets": tweets = searchForTweets(api,user,NBROFTWEETS)
else: sys.exit(COMMAND+": unknown task!")
printList(tweets)

