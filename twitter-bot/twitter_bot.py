import sys
from TwitterAPI import TwitterAPI

consumer_key = "<FILL IN>"
consumer_secret = "<FILL IN>"
access_token_key = "<FILL IN>"
access_token_secret = "<FILL IN>"
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

tweetList = []
twittersToRT = [""]