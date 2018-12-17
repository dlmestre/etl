from utils.setconfig import OpsConfiguration
from utils.authhandler import AuthConfig
from datacache.rediscache import RedisHandler
from twitter.twitterstreamer import LaunchStreamer
from twitter.tweetparser import ParseTweet
from utils.loggingconfig import LogConfiguration


class TwitterInit:

    track = ['Trump', 'pizza']
    words_filtered = []

    def __init__(self):
        LogConfiguration.set_logging()
        config_parser = OpsConfiguration.set_config()
        api = AuthConfig.load_api(config_parser['twitter'])
        self.redis_loader = RedisHandler(config_parser['redis'])
        LaunchStreamer.launch_streamer(api, self.track)

    def get_tweets(self):
        return [ParseTweet(tweet, self.words_filtered) for tweet in self.redis_loader.read()]

    def get_track(self):
        return self.track

    @staticmethod
    def get_hashtags(tweets, sentiment_limit=0.2):
        """TODO get most negative/positive hashtags"""
        pass
