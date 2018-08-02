'''Go through queue of retweets constantly'''
import tweepy
from queue import Queue
from random import randint, sample

#Variables for special actions
twitters_to_tag = ["@HannaBara", "@duredad",
                   "@DarrenGuyaz", "@Darnluxe", "@TiltedCS"]
trade_url = ("xxxxxxxxxxxxxxxxxxxxxxx" +
             "xxxxxxxxxxxxxxxxxxxxxxx")
drake_aff = "xxxxxxxxxxxxxxxxxxxxxxx"

def retweet(API, DONE, Q):
    #Get a tweet from the shared queue and retweet
    tweet = Q.get(True)
    id = tweet[0]
    opt = tweet[1]
    success = False
    #Try to rt until it works unless it's b&
    while not success:
        try:
            API.retweet(id)
            success = True
        except tweepy.TweepError as e:    
            print('*---%s' % e, flush=True)
            return DONE
    #Check for extra stuff and do it
    if any(entry for entry in opt.values()):
        msg = "@" + opt['user']
        if opt['tag']:
            #Make a sample and get users from the users list
            users = sample(range(len(twitters_to_tag)), 2)
            msg += (" " +
                    twitters_to_tag[int(users[0])] + " " +
                    twitters_to_tag[int(users[1])])
        if opt['url']:
            msg += " " + trade_url
        if opt['drake_aff']:
            msg += " " + drake_aff
        if opt['like']:
            try:
                API.create_favorite(id)
            except tweepy.TweepError as e:
                print('*---Like failed with %s' % e, flush=True)
        #Try to post reply
        try:
            API.update_status(status=msg, in_reply_to_status_id=id)
        except tweepy.TweepError as e:
            print('*---Reply failed with %s' % e, flush=True)
    #Mark tweet as done then remove it from queue and exit thread
    DONE[id] = True 
    Q.task_done()
    return DONE