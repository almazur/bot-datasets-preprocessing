class TweetMetrics:
    def __init__(self, user_id,  # TODO: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
                 number_of_tweets_last_x_days: int = None,  # TODO: determine x, IMPORTANT! x days from captured_at?
                 num_links_in_last_x_tweets: int = None,  # TODO: average from x tweets? IMPORTANT! last x tweets before captured_at?
                 num_hashtags_in_last_x_tweets: int = None,  # TODO: same as above
                 num_emojis_in_last_x_tweets: int = None,  # TODO: same as above
                 # TODO: location?
                 # TODO: tweet timestamp
                 ):
        pass