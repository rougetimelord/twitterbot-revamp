import sys
import tweepy
import time

consumer_key = "<FILL IN>"
consumer_secret = "<FILL IN>"
access_token_key = "<FILL IN>"
access_token_secret = "<FILL IN>"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

twitters_to_rt = ["SkinDotTrade", "skinhub", "SteamAnalyst"]
words_to_rt = ["giveaway", "contest", "enter", "rt"]

num_entered = 0

def retweet(id):
        success = False
        fails = 0
        while success  == False:
            try:
                r = api.retweet(id);
                if r.retweeted == "True":
                    success = True
                    num_entered += 1
            except tweepy.TweepError as e:
                fails += 1
                if fails >= 5 or e.api_code == 327:
                    print(e)
                    print("Really failed retweeting")
                    success = True
                time.sleep(10)

def uni_norm(text):
    return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22,
                            0xa0:0x20 })

def getNewestTweets(user):
    tweets = []
    rt = []
    told_user = False
    for tweet in api.user_timeline(screen_name = user,count=20):
        text = uni_norm(tweet.text).lower()
        if any(x in text for x in words_to_rt) and 'thank' not in text:
            rt.append(tweet.id_str)
            if 'reply' in text and told_user == False:
                told_user = True
                print('Check @%s for a reply entry' % user)

    for id in rt:
        retweet(id)

def startTweeting():
    print("Starting bot")
    run = 0
    while 1 >= 0:
        num_entered = 0
        for user in twitters_to_rt:
            getNewestTweets(user)
        run += 1
        print("Entered %s contests on run %s, now sleeping for an hour" % (num_entered, run))
        time.sleep(3600)

if __name__ == '__main__':
    startTweeting()