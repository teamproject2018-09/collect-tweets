import tweepy
import definitions

USER = "esciencecenter"
NBROFTWEETS = 200

def authenticate():
    # source: https://tweepy.readthedocs.io/en/v3.6.0/
    auth = tweepy.OAuthHandler(definitions.consumer_key,
                               definitions.consumer_secret)
    auth.set_access_token(definitions.token,
                          definitions.token_secret)
    return(auth)

def limit_handled(cursor):
    while True: 
        try: yield cursor.next()
        except tweepy.RateLimitError: time.sleep(15 * 60)

def getAllTweets(api,userName,count):
    tweetList = []
    for status in limit_handled(tweepy.Cursor(api.user_timeline,
                                              screen_name=userName,
                                              count=count)).items(): 
        tweetList.append(status._json)
    return(tweetList)

def searchForTweets(api,query,count):
    tweetList = []
    for status in tweepy.Cursor(api.search,
                                q=query,
                                count=count).items(): 
        tweetList.append(status._json)
    return(tweetList)

def printList(thisList):
    for t in thisList: print(t)
    return()

auth = authenticate()
api = tweepy.API(auth)
# tweets = getAllTweets(api,USER,NBROFTWEETS)
tweets = searchForTweets(api,USER,NBROFTWEETS)
printList(tweets)

