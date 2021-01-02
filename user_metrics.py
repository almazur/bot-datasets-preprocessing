from user import User


class UserMetrics:
    def __init__(self, user_id,
                 user_age: int = None,
                 tweets_count: int = None,
                 favourites_count: int = None,
                 followers_count: int = None,
                 listed_count: int = None,
                 friends_count: int = None,
                 replies_count: int = None,
                 mentions_count: int = None,
                 retweets_count: int = None,
                 times_retweeted: int = None,
                 tweet_freq: float = None,
                 followers_growth_rate: float = None,
                 friends_growth_rate: float = None,
                 favourites_growth_rate: float = None,
                 listed_growth_rate: float = None,
                 username_length: int = None,
                 name_length: int = None,
                 num_digits_in_username: int = None,
                 num_digits_in_name: int = None,
                 description_length: int = None,
                 followers_friends_ratio: float = None,
                 # screen_name_likelyhood - need to calculate
                 # profile_use_background_image - deprecated
                 ):
        self.user_id = user_id
        self.account_age = user_age,
        self.tweets_count = tweets_count,
        self.favourites_count = favourites_count,
        self.followers_count = followers_count,
        self.listed_count = listed_count,
        self.friends_count = friends_count,
        self.replies_count = replies_count,
        self.mentions_count = mentions_count,
        self.retweets_count = retweets_count,
        self.times_retweeted = times_retweeted,
        self.tweet_freq = tweet_freq,
        self.followers_growth_rate = followers_growth_rate,
        self.friends_growth_rate = friends_growth_rate,
        self.favourites_growth_rate = favourites_growth_rate,
        self.listed_growth_rate = listed_growth_rate,
        self.username_length = username_length,
        self.name_length = name_length,
        self.num_digits_in_username = num_digits_in_username,
        self.num_digits_in_name = num_digits_in_name,
        self.description_length = description_length,
        self.followers_friends_ratio = followers_friends_ratio


class UserMetricsBuilder:
    @classmethod
    def for_user(cls, user: User) -> UserMetrics:
        return UserMetrics(user_id=user.user_id,
                           user_age=user.age,
                           tweets_count=user.tweets_count,
                           favourites_count=user.favourites_count,
                           followers_count=user.followers_count,
                           listed_count=user.listed_count,
                           friends_count=user.friends_count,
                           replies_count=None,  # TODO part of user? add growth rate?
                           mentions_count=None,  # TODO part of user? add growth rate?
                           retweets_count=None,  # TODO part of user? add growth rate?
                           times_retweeted=None,  # TODO part of user? add growth rate?
                           tweet_freq=cls.check_none(lambda: user.tweets_count / user.age),
                           followers_growth_rate=cls.check_none(lambda: user.followers_count / user.age),
                           friends_growth_rate=cls.check_none(lambda: user.friends_count / user.age),
                           favourites_growth_rate=cls.check_none(lambda: user.favourites_count / user.age),
                           listed_growth_rate=cls.check_none(lambda: user.listed_count / user.age),
                           username_length=cls.check_none(lambda: len(user.user_name)),
                           name_length=cls.check_none(lambda: len(user.name)),
                           num_digits_in_username=cls.check_none(
                               lambda: sum([1 for l in user.user_name if l.isdigit()])),
                           num_digits_in_name=cls.check_none(lambda: sum([1 for l in user.name if l.isdigit()])),
                           description_length=cls.check_none(lambda: len(user.description)),
                           followers_friends_ratio=cls.check_none(lambda: user.followers_count / user.friends_count))

    @classmethod
    def check_none(cls, operation):
        try:
            return operation()
        except TypeError as e:
            return None
