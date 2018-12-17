from flask import Flask, render_template
from backend import TwitterInit
from utils.parsetrack import ParseTracks

app = Flask(__name__)
twitter_initialize = TwitterInit()


@app.route('/')
def index():
    tweets = twitter_initialize.get_tweets()
    track = twitter_initialize.get_track()
    return render_template('index.html', tweets=tweets, track=ParseTracks(track))


if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=True, debug=True)
