import tweepy
import time
import csv
import os
from random import randint
from hashlib import sha256
import datetime

consumer_key = "<FILL IN>"
consumer_secret = "<FILL IN>"
access_token_key = "<FILL IN>"
access_token_secret = "<FILL IN>"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

twitters_to_rt = ["SkinDotTrade", "skinhub", "SteamAnalyst", "CSGO500", 
    "CSGOatsecom", "Society_gg", "hellcasecom", "CSGOExclusive", "earnggofficial",
    "DrakeMoon", "csgomassive", "CSGODerby", "skinupgg"]
twitters_to_tag = ["@HannaBara", "@duredad"]
trade_url = "https://steamcommunity.com/tradeoffer/new/?partner=126854537&token=7bID1Tq5"
words_to_rt = ["giveaway", "contest", "enter", "rt"]
blocked_words = ["thank", "winning", "congrats", "winner of", "winners of", "profile url", "affi"]

num_entered = 0
tweet_floor = 70

def retweet(id, opt):
    success = False
    fails = 0
    rand = randint(1,100)
    if rand >= tweet_floor:
        text = sha256(datetime.datetime.now().strftime('%Y:%m:%d_%H:%M:%S').encode('utf-8')).hexdigest()[:7]
        try:
            api.update_status(text)
        except tweepy.TweepError as e:
            print(e)
        print('Waiting %s seconds' % (rand * 2))
        time.sleep(rand*2)
    while success == False:
        try:
            r = api.retweet(id)
            api.create_favorite(id)
            num_entered += 1
            success = True
        except tweepy.TweepError as e:
            fails += 1
            if fails >= 5 or e.api_code == 327:
                print(e)
                success = True
            time.sleep(10)
    if opt['tag'] == True or opt['url'] == True:
        msg = "@" + opt['user']
        if opt['tag'] == True:
            msg += " " + twitters_to_tag[0] + " " + twitters_to_tag[1]
        if opt['url'] == True:
            msg += " " + trade_url
        try:
            api.update_status(status = msg, in_reply_to_status_id = id)
        except tweepy.TweepError as e:
            print('Reply failed with %s' % e)
    return

def uni_norm(text):
    return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22,
                            0xa0:0x20 })

def getNewestTweets(user, done):
    tweets = []
    for tweet in api.user_timeline(screen_name = user,count = 5,exclude_replies='true',include_rts='false'):
        extras = {'user': "",'tag': False,'url': False}
        tweet_id = tweet.id_str
        if tweet_id in done:
            continue
        tweet_text = uni_norm(tweet.text).lower()
        done.append(tweet_id)
        if any(x in tweet_text for x in words_to_rt):   
            if any(y in tweet_text for y in blocked_words):
                continue
            if any(z in tweet_text for z in ['reply', 'tag', 'paste']):
                extras['user'] = user
                if 'tag' in tweet_text:
                    extras['tag'] = True
                if 'trade' in tweet_text:
                    extras['url'] = True
            retweet(tweet_id, extras)

def startTweeting():
    print('Loading processed tweets')
    with open('done_list.csv', 'r') as f:
        reader = csv.reader(f)
        temp = list(reader)
        if len(temp) > 0:
            done = temp[0]

    print("Starting bot")
    run = 0
    go = True
    while go:
        run += 1
        print("Running run %s" % run)
        num_entered = 0
        for user in twitters_to_rt:
            getNewestTweets(user, done)
        tweet_floor = randint(30, 80)

        os.remove('done_list.csv')
        with open('done_list.csv', 'w', newline='') as file:
            w = csv.writer(file)
            w.writerow(done)

        wait_m = randint(10,60)
        print("Entered %s contests on run %s, now sleeping for %s minutes\
            \nPress Ctrl+C to exit" % (num_entered, run, wait_m))
        wait_s = 60 * wait_m
        for i in range(wait_s):
            try:
                time.sleep(1)
                if i % 300 == 0 and not i == 0:
                    print("5 minutes passed")
            except KeyboardInterrupt as e:
                go = False

if __name__ == '__main__':
    startTweeting()