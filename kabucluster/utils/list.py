from glob import glob
import os
import tweepy
from kabucluster import settings

auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_KEY, settings.ACCESS_SECRET)
api = tweepy.API(auth)


for filename in glob('./users/*.txt'):
    list_id = os.path.splitext(os.path.basename(filename))[0]
    with open(filename) as f:
        for screen_name in f.readlines():
            screen_name = screen_name.strip()
            print(screen_name)
            try:
                api.add_list_member(list_id=list_id, screen_name=screen_name)
            except tweepy.TweepError as e:
                print(e)