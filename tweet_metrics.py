from tweet import Tweet
from tweet_downloader import TweetCollection
import emoji
import regex


class TweetMetrics:
    def __init__(self, user_id,
                 # TODO: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
                 number_of_tweets_last_x_days: int = None,  # TODO: determine x, counting from now or user's 'captured_at'? what if no tweets found? Search by different dates?
                 num_links_per_tweet_from_last_x_tweets: int = None,
                 num_hashtags_per_tweet_from_last_x_tweets: int = None,
                 num_emojis_per_tweet_from_last_x_tweets: int = None,
                 # TODO: tweet timestamp metric?
                 ):
        self.user_id = user_id
        self.number_of_tweets_last_x_days = number_of_tweets_last_x_days
        self.num_links_per_tweet_from_last_x_tweets = num_links_per_tweet_from_last_x_tweets
        self.num_hashtags_per_tweet_from_last_x_tweets = num_hashtags_per_tweet_from_last_x_tweets
        self.num_emojis_per_tweet_from_last_x_tweets = num_emojis_per_tweet_from_last_x_tweets


class TweetMetricsBuilder:
    @classmethod
    def for_user_tweets(cls, user_id: str, tweets: TweetCollection) -> TweetMetrics:
        last_x_tweets = tweets.last_x_tweets
        links_avg = cls.calc_average(cls.retrieve_number_of_links, last_x_tweets)
        hashtags_avg = cls.calc_average(cls.retrieve_number_of_hashtags, last_x_tweets)
        emojis_avg = cls.calc_average(cls.retrieve_number_of_emojis, last_x_tweets)
        return TweetMetrics(user_id=user_id,
                            number_of_tweets_last_x_days=len(tweets.x_days_tweets),
                            num_links_per_tweet_from_last_x_tweets=links_avg,
                            num_hashtags_per_tweet_from_last_x_tweets=hashtags_avg,
                            num_emojis_per_tweet_from_last_x_tweets=emojis_avg)

    @classmethod
    def calc_average(cls, per_tweet_metric_function, tweets):
        return None if len(tweets) == 0 else sum([per_tweet_metric_function(t) for t in tweets]) / len(tweets)  # TODO

    @classmethod
    def retrieve_number_of_links(cls, tweet: Tweet):
        return len(tweet.urls)

    @classmethod
    def retrieve_number_of_hashtags(cls, tweet: Tweet):
        return len(tweet.hashtags)

    @classmethod
    def retrieve_number_of_emojis(cls, tweet: Tweet):
        emoji_list = []
        data = regex.findall(r'\X', tweet.content)
        for word in data:
            if any(char in emoji.UNICODE_EMOJI for char in word):
                emoji_list.append(word)
        return len(emoji_list)
