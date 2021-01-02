from cassandra.cluster import Cluster

from tweet import Tweet
from user import User


class CassandraService:

    def __init__(self, keyspace='data'):
        self.session = Cluster().connect(keyspace)
        self.user_insert_stmt = self.prepare_user_insert_statement()
        self.tweet_insert_stmt = self.prepare_tweet_insert_statement()
        self.exception_insert_stmt = self.prepare_exception_insert_statement()

    def save_user(self, user: User):
        self.session.execute(self.user_insert_stmt, vars(user))

    def save_tweet(self, tweet: Tweet):
        self.session.execute(self.tweet_insert_stmt, vars(tweet))

    def save_exception(self, exception_data: dict):
        self.session.execute(self.exception_insert_stmt, exception_data)

    def prepare_user_insert_statement(self):
        return self.session.prepare(
            """
            INSERT INTO pronbots_2019 (id, captured_at, created_at, description, entities, favourites_count,
                followers_count, following_count, friends_count, listed_count, name, pinned_tweet_id, profile_image_url,
                protected, tweets_count, url, user_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        )

    def prepare_tweet_insert_statement(self):
        return self.session.prepare(
            """
            INSERT INTO pronbots_2019_tweets (id, captured_at, created_at, user_id, timezone, content, link, retweet,
                mentions, urls, photos, video, lang, replies_count, retweets_count, likes_count, hashtags, cashtags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        )

    def prepare_exception_insert_statement(self):
        return self.session.prepare(
            """
            INSERT INTO pronbots_2019_exceptions (user, exception)
            VALUES (?, ?)
            """
        )
