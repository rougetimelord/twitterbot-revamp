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
#set up API
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
    C_threads = []
    while(True):
        if not Q.empty and Q.qsize >= 4:
            print('Spawning 4 retweet threads')
            for i in range(0, 4):
                thread_obj = threading.Thread(target=consume_wrapper)
                C_threads.append(thread_obj)
                thread_obj.start()
                print('--Spawned thread %s' % i)
                sleep(randint(60, 600))

def feed_wrapper():
    print('Feed thread spawned')
    global DONE
    while True:
        DONE = find_tweets.getUserTweets(API, DONE, Q)
        with open('done.json', 'w', newline='') as f:
            json.dump(DONE, f)
        sleep(300)

def consume_wrapper():
    global DONE
    DONE = retweet.retweet(API, DONE, Q)
    with open('done.json', 'w', newline='') as f:
        json.dump(DONE, f)
    return

if __name__ == '__main__':
    bot()