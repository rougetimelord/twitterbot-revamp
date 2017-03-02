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
    "CSGOatsecom", "Society_gg", "hellcasecom"]
words_to_rt = ["giveaway", "contest", "enter", "rt"]
blocked_words = ["thank", "winning", "congrats", "winner of"]

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

def getNewestTweets(user, done):
    tweets = []
    told_user = False
    for tweet in api.user_timeline(screen_name = user,count = 5,exclude_replies='true',include_rts='false'):
        tweet_id = tweet.id_str
        if tweet_id in done:
            print("Skipping %s" % tweet.id_str)
            continue
        tweet_text = uni_norm(tweet.text).lower()
        done.append(tweet_id)
        if any(x in tweet_text for x in words_to_rt):   
            if any(y in tweet_text for y in blocked_words):
                continue
            retweet(tweet_id)
            if 'reply' in tweet_text and told_user == False:
                told_user = True
                print('Check @%s for a reply entry' % user)

def startTweeting():
    print('Loading processed tweets')
    with open('done_list.csv', 'r') as f:
        reader = csv.reader(f)
        temp = list(reader)
        if len(temp) > 0:
            done = temp[0]

    print("Starting bot")
    run = 0
    while 1 >= 0:
        print("Running run %s" % run)
        num_entered = 0
        for user in twitters_to_rt:
            getNewestTweets(user, done)
        run += 1
        print("Entered %s contests on run %s, now sleeping for an hour \
            \n Press Ctrl+C to write finished tweets and exit" % (num_entered, run))
        for i in range(3600):
            try:
                time.sleep(1)
                if i % 300 == 0 and not i == 0:
                    print("5 minutes passed")
            except KeyboardInterrupt as e:
                os.remove('done_list.csv')
                with open('done_list.csv', 'w', newline='') as file:
                    w = csv.writer(file)
                    w.writerow(done)
                input("Press Enter to exit...")
                sys.exit(0)

if __name__ == '__main__':
    startTweeting()
