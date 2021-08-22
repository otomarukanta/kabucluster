import tweepy

from kabucluster import settings

def get_auth():
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)

    try:
        redirect_url = auth.get_authorization_url()
        print(redirect_url)
        verifier = input('Verifier:')
    except tweepy.TweepError as e:
        raise e

    key, secret = auth.get_access_token(verifier)
    print(key, secret)