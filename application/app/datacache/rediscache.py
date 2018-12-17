import json
import logging
import redis
import os

log = logging.Logger(__name__)


class SingletonHandler(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(SingletonHandler, cls).__call__(*args, **kwargs)
        return cls.instance


class RedisHandler(metaclass=SingletonHandler):

    redis_key = 'tweets'
    num_tweets = 30
    trim_threshold = 50000

    def __init__(self, config):
        self.db = r = redis.Redis(
            host=config.get('host', vars=os.environ),
            port=config.get('port', vars=os.environ),
            password=config.get('password', vars=os.environ)
        )
        self.trim_count = 0

    def read(self, limit=15):
        for item in self.db.lrange(self.redis_key, 0, limit-1):
            yield json.loads(item)

    def push(self, data):
        self.db.lpush(self.redis_key, json.dumps(data))
        self.trim_count += 1
        if self.trim_count > self.trim_threshold:
            self.db.ltrim(self.redis_key, 0, self.num_tweets)
            self.trim_count = 0
