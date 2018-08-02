'''Find new tweets and append them to the  queue'''
import tweepy, re
from queue import Queue

#Tweet variables
twitters_to_rt = ['skinhub', 'SteamAnalyst', 'CSGO500',
                  'CSGOatsecom', 'Society_gg', 'hellcasecom',
                  'CSGOExclusive', 'earnggofficial', 'DrakeMoon',
                  'csgomassive', 'CSGODerby', 'skinupgg', 'flashyflashycom', 'RaffleTrade', 'SteamGems', 'zevoCSGO']
words_to_rt = ["giveaway", "contest", "enter", "rt", "luck"]
special_words = ['reply', 'tag', 'trade', 'affi', 'sub', 'follow', 'like']
blocked_words = ["thank", "winning", "congrat",
                 "dm", "profile url", "vote", "won"]
re_pat = r'((?<=@)|(?<=@ ))([\w]*)'

#Normalize unicode
def uni_norm(text):
    return text.translate({0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22,
                          0xa0:0x20})

#Search user's timeline for tweets that we want
def getNewestTweets(user, API, done, Q):
    print("Scraping %s" % user)
    #Try to get timeline
    try:
        tweets = API.user_timeline(screen_name=user,
                                   count=5, exclude_replies='true',
                                   include_rts='false', tweet_mode='extended')
    except tweepy.TweepError as e:
        print(e)
        return done
    #Check for extra features
    for tweet in tweets:
        extras = {'user': "", 'tag': False,
                  'url': False, 'drake_aff': False, 'like': False}
        tweet_id = tweet.id_str
        if tweet_id in done:
            continue
        tweet_text = uni_norm(tweet.full_text).lower()
        if any(x in tweet_text for x in words_to_rt):
            if any(y in tweet_text for y in blocked_words):
                continue
            if any(z in tweet_text for z in special_words):
                extras['user'] = user
                if 'tag' in tweet_text:
                    extras['tag'] = True
                if 'trade' in tweet_text:
                    extras['url'] = True
                if 'affi' in tweet_text and user == "DrakeMoon":
                    extras['drake_aff'] = True
                if 'sub' in tweet_text:
                    print("%s wants to get a subscriber" % user)
                if 'follow' in tweet_text:
                    follow_list = re.findall(re_pat, tweet_text)
                    for u in follow_list:
                        try:
                            API.create_friendship(id=u)
                        except tweepy.TweepError as e:
                            print(e)
                if 'like' in tweet_text:
                    extras['like'] = True
            done[tweet_id] = False
            Q.put((tweet_id, extras), True)
    return done

#Go through all users and then search
def getUserTweets(API, done, Q):
    for user in twitters_to_rt:
        done = getNewestTweets(user, API, done, Q)
    return done