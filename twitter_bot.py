import tweepy
import json
import os
import key
import find_tweets, retweet
import threading
from queue import Queue
from time import sleep
from random import randint

print('Setting up key')
consumer_key = key.con_k()
consumer_secret = key.con_s()
access_key = key.acc_k()
access_secret = key.acc_s()
AUTH = tweepy.OAuthHandler(consumer_key, consumer_secret)
AUTH.set_access_token(access_key, access_secret)
API = tweepy.API(AUTH)
Q = Queue()
print('Key set \nLoading list of done tweets')

try:
    with open('done.json', 'r') as f:
            DONE = json.load(f)
except IOError:
    with open('done.json', 'w') as f:
            DONE = {}
print("Loaded done tweets")

def bot():
    print('Bot started')
    f_thread = threading.Thread(group=None, target=feed_wrapper, name="Feed", args=(), kwargs={})
    f_thread.start()
    #Spawn pool of retweet.py consumer threads here, i possible restart on returns
    f_thread.join()

def feed_wrapper():
    global DONE
    while True:
        DONE = find_tweets.getUserTweets(API, DONE, Q)
        with open('done.json', 'w', newline='') as f:
            json.dump(DONE, f)
        sleep(300)

def consume_wrapper():
    global DONE
    while True:
        retweet.retweet(API, DONE, Q)
        with open('done.json', 'w', newline='') as f:
            json.dump(DONE, f)
        sleep(300)

if __name__ == '__main__':
    bot()