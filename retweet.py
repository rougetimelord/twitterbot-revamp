'''Go through queue of retweets constantly'''
import tweepy
import re
import time
from queue import Queue
from random import randint, sample

twitters_to_tag = ["@HannaBara", "@duredad",
                   "@DarrenGuyaz", "@Darnluxe", "@TiltedCS"]
trade_url = ("https://steamcommunity.com/tradeoffer/" +
             "new/?partner=126854537&token=7bID1Tq5")
drake_aff = "https://www.drakemoon.com/promo-code/r0uge"
def retweet(API, DONE, Q):
    tweet = Q.get(True)
    id = tweet[0]
    opt = tweet[1]
    success = False
    fails = 0
    while not success:
        try:
            API.retweet(id)
            success = True
        except tweepy.TweepError as e:
            fails += 1
            if fails >= 5 or e.api_code == 327:
                print(e)
                success = True
            time.sleep(10)
    if any(entry for entry in opt.values()):
        msg = "@" + opt['user']
        if opt['tag']:
            users = sample(range(len(twitters_to_tag)), 2)
            a = int(users[0])
            b = int(users[1])
            msg += (" " +
                    twitters_to_tag[a] + " " +
                    twitters_to_tag[b])
        if opt['url']:
            msg += " " + trade_url
        if opt['drake_aff']:
            msg += " " + drake_aff
        if opt['like']:
            try:
                API.create_favorite(id)
            except tweepy.TweepError as e:
                print('Like failed with %s' % e)
        try:
            API.update_status(status=msg, in_reply_to_status_id=id)
        except tweepy.TweepError as e:
            print('Reply failed with %s' % e)
    DONE[id] = True
    time.sleep(randint(30, 1800))
    Q.task_done()
    return DONE