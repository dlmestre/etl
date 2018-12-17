import tweepy
import os


class AuthConfig:
    @staticmethod
    def load_api(config):
        consumer_key = config.get('consumer_key', vars=os.environ)
        consumer_secret = config.get('consumer_secret', vars=os.environ)
        access_token = config.get('access_token', vars=os.environ)
        access_token_secret = config.get('access_token_secret', vars=os.environ)

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        auth.set_access_token(access_token, access_token_secret)

        return tweepy.API(auth)
