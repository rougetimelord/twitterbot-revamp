import sys
from TwitterAPI import TwitterAPI

consumer_key = "<FILL IN>"
consumer_secret = "<FILL IN>"
access_token_key = "<FILL IN>"
access_token_secret = "<FILL IN>"
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

tweetList = []
twittersToRT = ["SkinDotTrade", "skinhub", "SteamAnalyst"]
wordsToRT = ["giveaway", "contest", "enter", "rt"]

def retweet(id):
        success = False
        while success  == False:
            try:
                r = api.request("statuses/retweet", 
                    {'id': id})
                if response.getcode() == 200:
                    success = True
            except Exception as e:
                print(e)
                time.sleep(5)
        return "Done"

def getNewestTweets(user):
    tweets = []
    rt = []
    for item in api.request("statuses/user_timeline", 
        {'screen_name': user}, {'count': 10}):
        tweets.append(item['id'], item['text'])

    for tweet in tweets:
        text = tweet[1].lower()
        if any(x in text for x in wordsToRT):
            rt.append(tweet[0])

    for id in rt:
        retweet(id)
        
    