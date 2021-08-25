from kabucluster.models import TweetToken
import re
from datetime import timedelta, datetime
import dataclasses
import itertools
import time
import threading

import tweepy
import neologdn
import MeCab
import emoji
from dataclass_csv import DataclassReader

from kabucluster import settings



@dataclasses.dataclass
class Tweet:
    id: str
    tweeted_at: datetime
    user_id: str
    screen_name: str
    text: str

@dataclasses.dataclass
class Token:
    tweet_id: str
    tweeted_at: datetime
    user_id: str
    screen_name: str
    token: str
    code: str

@dataclasses.dataclass
class Ticker:
    code: str
    name: str
    market_name: str
    topix_33_code: str = ''
    topix_33_name: str = ''
    topix_17_code: str = ''
    topix_17_name: str = ''
    topix_new_index_series_code: str = ''
    topix_new_index_series_name: str = ''


class Daemon:
    RE_URL = re.compile(r'https?:\/\/.*[\r\n]*')
    RE_MARK = re.compile('[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”◇ᴗ●↓→♪★⊂⊃※△□◎〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]')
    MECAB = MeCab.Tagger(f'-d {settings.NEOLOGD_PATH}')

    def __init__(self) -> None:
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_KEY, settings.ACCESS_SECRET)
        self.twitter = tweepy.API(auth)
        self.since_id = None

        with open(settings.STOPWORDS_PATH) as f:
            self.stop_words = f.read().splitlines()

        with open(settings.TICKERS_PATH) as f:
            reader = DataclassReader(f, Ticker)
            self.tickers = [x for x in reader] # type: list[Ticker]

    def fetch_tweets(self, list_id):
        raw_tweets = self.twitter.list_timeline(list_id=list_id, count=200, include_rts=False, since_id=self.since_id)
        tweets = [Tweet(
            id=tweet.id, tweeted_at=tweet.created_at + timedelta(hours=9), user_id=tweet.author.id,
            text=tweet.text, screen_name=tweet.author.screen_name)
            for tweet in raw_tweets]
        tweet_ids = [x.id for x in tweets]
        if tweet_ids:
            self.since_id = max(tweet_ids)
        return tweets

    def tokenize(self, tweet: Tweet) -> list[Token]:
        text = tweet.text
        text = ''.join([c for c in text if not c in emoji.UNICODE_EMOJI_ENGLISH])
        text = self.RE_URL.sub('', text)
        text = self.RE_MARK.sub('', text)
        text = neologdn.normalize(text)

        node = self.MECAB.parseToNode(text)
        tokens = []

        def _filter(token: str):
            if token in self.stop_words:
                return False
            if token.isdigit() and len(token) != 4:
                return False
            return True

        while node:
            token = node.surface
            pos = node.feature.split(',')[0]
            if pos in ['名詞'] and _filter(token):
                tokens.append(token)

            node = node.next
        
        return [Token(
            tweet_id=tweet.id, tweeted_at=tweet.tweeted_at, 
            user_id=tweet.user_id, screen_name=tweet.screen_name, token=t, code=''
         ) for t in tokens]
        

    def predict_ticker(self, token: Token):
        text = token.token
        if text.isdigit() and text in [x.code for x in self.tickers]:
            token.code = text

        if text in [x.name for x in self.tickers]:
            mapping = {x.name: x.code for x in self.tickers}
            token.code = mapping[text]
        return token

    def load(self, tokens):
        if len(tokens) == 0:
            return
        session = settings.session()
        session.execute(TweetToken.__table__.insert().prefix_with('IGNORE').values(tokens))
        session.commit()

    def run(self):
        for list_id in settings.TWITTER_LIST_IDS:
            tweets = self.fetch_tweets(list_id)
            tokens = itertools.chain.from_iterable([self.tokenize(tweet) for tweet in tweets])
            tokens = [self.predict_ticker(token) for token in tokens]
            tokens = [{
                'tweet_id': token.tweet_id, 'tweeted_at': token.tweeted_at, 'user_id': token.user_id,
                'screen_name': token.screen_name, 'token': token.token, 'code': token.code
            } for token in tokens]

            self.load([token for token in tokens if token['code']])
    

    def run_forever(self, interval = 5):
        base_time = time.time()
        next_time = 0
        while True:
            t = threading.Thread(target=self.run)
            t.start()
            next_time = ((base_time - time.time()) % interval) or interval
            time.sleep(next_time)

