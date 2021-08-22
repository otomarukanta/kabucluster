from datetime import timedelta
import threading
import time

from kabucluster.models.tweet import Tweet
from kabucluster import settings
import tweepy

class Collector:
    def __init__(self) -> None:
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_KEY, settings.ACCESS_SECRET)
        self.twitter = tweepy.API(auth)
        self.session = settings.session()
        self.since_id = None
    
    def extract(self, list_id):
        raw_tweets = self.twitter.list_timeline(list_id=list_id, count=200, include_rts=False, since_id=self.since_id)
        tweets = [{
            'id': tweet.id, 'tweeted_at': tweet.created_at + timedelta(hours=9), 'user_id': tweet.author.id,
            'user_name': tweet.author.name, 'text' :tweet.text
            } for tweet in raw_tweets]
        tweet_ids = [x['id'] for x in tweets]
        if tweet_ids:
            self.since_id = max(tweet_ids)
        return tweets

    def load(self, tweets):
        self.session.execute(Tweet.__table__.insert().prefix_with('IGNORE').values(tweets))
        self.session.commit()
    
    def run(self):
        for list_id in settings.TWITTER_LIST_IDS:
            tweets = self.extract(list_id)
            self.load(tweets)
    
    def run_forever(self, interval = 5):
        base_time = time.time()
        next_time = 0
        while True:
            t = threading.Thread(target=self.run)
            t.start()
            next_time = ((base_time - time.time()) % interval) or interval
            time.sleep(next_time)