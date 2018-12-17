import re
from datacache.rediscache import RedisHandler


class ParseTweet:

    def __init__(self, data, filtered_words):
        self.data = data
        self.filtered_words = filtered_words
        self.redis_data = RedisHandler()

    def user_link(self):
        return "https://twitter.com/{0}".format(self.data['username'])

    def filtered_text(self):
        return self._filter_words(self._filter_urls(self.data['text']))

    def _filter_words(self, text):
        for word in self.filtered_words:
            if (word in text):
                text = text.replace(word, "<mark>{0}</mark>".format(word))
            else:
                continue
        return text

    @staticmethod
    def _filter_urls(text):
        return re.sub("(https?:\/\/\w+(\.\w+)+(\/[\w\+\-\,\%]+)*(\?[\w\[\]]+(=\w*)?(&\w+(=\w*)?)*)?(#\w+)?)", r'<a href="\1" target="_blank">\1</a>', text)
