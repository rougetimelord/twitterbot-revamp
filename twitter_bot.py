import tweepy, json, os
import key, threading
import find_tweets, retweet
from queue import Queue
from time import sleep
from random import randint

#set up API
print('!-Setting up key', flush=True)
consumer_key = key.con_k()
consumer_secret = key.con_s()
access_key = key.acc_k()
access_secret = key.acc_s()
AUTH = tweepy.OAuthHandler(consumer_key, consumer_secret)
AUTH.set_access_token(access_key, access_secret)
API = tweepy.API(AUTH)

#Threading stuff
Q = Queue()
LOCK = threading.Lock()

#Load done list and put not done items in the queue 
print('!-Loading list of done tweets', flush=True)
try:
    with open('done.json', 'r') as f:
            DONE = json.load(f)
            for key, value in DONE.items():
                if not value:
                    Q.put((key, value))
except IOError:
    with open('done.json', 'w') as f:
            DONE = {}

def bot():
    print('!-Bot started', flush=True)
    #Make a feeder thread that runs constantly
    f_thread = threading.Thread(group=None, target=feed_wrapper, name="Feed", args=(), kwargs={})
    f_thread.start()
    #Periodically check if there's enough tweets to spawn a pool of threads
    C_threads = []
    while(True):
        if not Q.empty() and Q.unfinished_tasks >= 4:
            print('--Spawning 4 retweet threads', flush=True)
            for i in range(0, 4):
                thread_obj = threading.Thread(target=consume_wrapper)
                C_threads.append(thread_obj)
                thread_obj.start()
                print('!---Spawned thread %s' % i, flush=True)
                sleep(randint(30, 1800))

#Using wrappers is convenient because you don't need to pass args
#in your thread call. The wrappers just call the functions and pass
#variables (which are in scope for the wrapper, but not the function),
#then dump the done list to disk.
def feed_wrapper():
    print('!-Feed thread spawned', flush=True)
    global DONE
    while True:
        DONE = find_tweets.getUserTweets(API, DONE, Q)
        sleep(300)
        dumper()

def consume_wrapper():
    global DONE
    DONE = retweet.retweet(API, DONE, Q)
    dumper()
    return

#Dump to disk thread safely
def dumper():
    LOCK.acquire()
    try:
        with open('done.json', 'w', newline='') as f:
            json.dump(DONE, f)
    except IOError as e:
        print('!--%s' % e, flush=True)
    LOCK.release()
    return


if __name__ == '__main__':
    bot()