import sys
import tweepy
import time
import csv

consumer_key = "<FILL IN>"
consumer_secret = "<FILL IN>"
access_token_key = "<FILL IN>"
access_token_secret = "<FILL IN>"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

twitters_to_rt = ["SkinDotTrade", "skinhub", "SteamAnalyst", "CSGO500", 
    "CSGOatsecom", "Society_gg"]
words_to_rt = ["giveaway", "contest", "enter", "rt"]
blocked_words = ["thank", "winning", "congrats"]

done = []

num_entered = 0

def retweet(id):
    if id in done:
        return ''
    success = False
    fails = 0
    while success  == False:
        try:
            r = api.retweet(id);
            if r.retweeted == "True":
                success = True
                num_entered += 1
                done.append(id)
        except tweepy.TweepError as e:
            fails += 1
            if fails >= 5 or e.api_code == 327:
                print(e)
                print("Really failed retweeting")
                success = True
                done.append(id)
            time.sleep(10)

def uni_norm(text):
    return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22,
                            0xa0:0x20 })

def getNewestTweets(user):
    tweets = []
    rt = []
    told_user = False
    for tweet in api.user_timeline(screen_name = user,count=5):
        text = uni_norm(tweet.text).lower()
        if any(x in text for x in words_to_rt) and not any(y in text for y in blocked_words):
            rt.append(tweet.id_str)
            if 'reply' in text and told_user == False:
                told_user = True
                print('Check @%s for a reply entry' % user)

    for id in rt:
        retweet(id)

def startTweeting():
    with open('done_list.csv', 'r') as f:
        reader = csv.reader(f)
        if len(list(reader)) > 0:
            done = list(reader)[0]

    
    print("Starting bot")
    run = 0
    while 1 >= 0:
        num_entered = 0
        for user in twitters_to_rt:
            getNewestTweets(user)
        run += 1
        print("Entered %s contests on run %s, now sleeping for an hour" % (num_entered, run))
        for i in range(3600):
            try:
                sleep(1)
            except KeyboardInterrupt as e:
                with open('done_list.csv', 'w', newline='') as file:
                    w = csv.writer(file)
                    w.truncate()
                    w.writerow(done)
                sys.exit()

if __name__ == '__main__':
    startTweeting()