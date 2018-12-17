import tweepy
from tweepy.streaming import StreamListener
import datetime
from textblob import TextBlob
from datacache.rediscache import RedisHandler
import langdetect
import logging

log = logging.Logger(__name__)


class StreamListener(tweepy.StreamListener):

    def __init__(self):
        super().__init__()
        self.cache = RedisHandler()

    def on_status(self, status):

        try:
            if 'RT @' not in status.text and len(status.text) > 50 and langdetect.detect(status.text) == 'en':
                blob = TextBlob(status.text)
                sent = blob.sentiment
                polarity = sent.polarity
                subjectivity = sent.subjectivity
                words_of_interest = [item[0] for item in blob.pos_tags if item[1] == 'JJ' or item[1] == 'NN']

                tweet_item = {
                    'id_str': status.id_str,
                    'text': status.text,
                    'words_of_interest': words_of_interest,
                    'polarity': polarity,
                    'subjectivity': subjectivity,
                    'username': status.user.screen_name,
                    'name': status.user.name,
                    'profile_image_url': status.user.profile_image_url,
                    'received_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.cache.push(tweet_item)
                log.debug("Pushed to redis:", tweet_item)
        except Exception as e:
            log.error(e)

    def on_error(self, status_code):
        if status_code == 420:
            return False


class LaunchStreamer:
    @staticmethod
    def launch_streamer(api, track):
        stream_listener = StreamListener()
        stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
        stream.filter(track=track, async=True)
