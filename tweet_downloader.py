import twint
from datetime import datetime, timedelta
import math
from tweet import TweetBuilder


class TweetCollection:
    def __init__(self, tweets_from_x_days, remaining_tweets, x):
        self.tweets = tweets_from_x_days + remaining_tweets
        self.x_days_index = len(tweets_from_x_days)
        self.x_tweets_index = x if len(remaining_tweets) == 0 else len(self.tweets)

    @property
    def last_x_tweets(self):
        return self.tweets[:self.x_tweets_index]

    @property
    def x_days_tweets(self):
        return self.tweets[:self.x_days_index]

    @property
    def all(self):
        return self.tweets


class TweetDownloader:

    def __init__(self, min_tweet_count=100, min_tweet_period=100, hide_output=False):
        self.twint_date_format = '%Y-%m-%d'
        self.twint_increments_base = 100
        self.min_tweet_count = min_tweet_count
        self.min_tweet_period = min_tweet_period
        self.hide_output = hide_output

    def download(self, user_id: str, base_date: datetime):
        # search for tweets from 'base_date - min_tweet_period' to 'base_date'
        tweets_start_date = base_date - timedelta(days=self.min_tweet_period)
        self.search(user_id, since=tweets_start_date, until=base_date)
        tweets_from_x_days = self.pop_tweets_from_storage()

        # if fetched less than 'min_tweet_count' download remaining tweets from before 'base_date - min_tweet_period'
        fetched_count = len(tweets_from_x_days)
        remaining_tweets = []
        if fetched_count < self.min_tweet_count:
            to_fetch = self.min_tweet_count - fetched_count
            self.search(user_id, until=tweets_start_date, limit=self.ceil(to_fetch, self.twint_increments_base))
            remaining_tweets = self.pop_tweets_from_storage()[:to_fetch]
        captured_at = datetime.now()

        x_days_tweets = [TweetBuilder.from_twint(t, captured_at) for t in tweets_from_x_days]
        x_remaining_tweets = [TweetBuilder.from_twint(t, captured_at) for t in remaining_tweets]
        return TweetCollection(tweets_from_x_days=x_days_tweets, remaining_tweets=x_remaining_tweets,
                               x=self.min_tweet_count)

    def search(self, user_id, since=None, until=None, limit=None):
        c = twint.Config()
        c.User_id = user_id
        if until is not None:
            c.Until = self.as_string(until)
        if since is not None:
            c.Since = self.as_string(since)
        if limit is not None:
            c.Limit = limit
        c.Hide_output = self.hide_output
        c.Store_object = True
        twint.run.Search(c)

    @staticmethod
    def pop_tweets_from_storage():
        tweets = twint.output.tweets_list
        twint.output.tweets_list = []
        return tweets

    def as_string(self, dt):
        return dt.strftime(self.twint_date_format)

    @staticmethod
    def ceil(x, base):
        return base * math.ceil(x / base)
