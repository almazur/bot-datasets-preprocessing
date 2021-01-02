from datetime import datetime
import json


class User:
    def __init__(self, user_id: str, captured_at: datetime,
                 created_at: datetime = None,
                 description: str = None,
                 entities: str = None,
                 favourites_count: int = None,
                 followers_count: int = None,
                 following_count: int = None,
                 friends_count: int = None,
                 listed_count: int = None,
                 name: str = None,
                 pinned_tweet_id: str = None,
                 profile_image_url: str = None,
                 protected: bool = None,
                 tweets_count: int = None,
                 url: str = None,
                 user_name: str = None,
                 ):
        # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/overview/user-object
        # https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/quick-start
        self.id = user_id
        self.captured_at = captured_at
        self.created_at = created_at
        self.description = description
        self.entities = entities
        self.favourites_count = favourites_count
        self.followers_count = followers_count
        self.following_count = following_count
        self.friends_count = friends_count
        self.listed_count = listed_count
        self.name = name
        self.pinned_tweet_id = pinned_tweet_id
        self.profile_image_url = profile_image_url
        self.protected = protected
        self.tweets_count = tweets_count
        self.url = url
        self.user_name = user_name

    @property
    def user_id(self):
        return self.id

    @property
    def age(self):
        return (self.captured_at - self.created_at).days

    def __repr__(self):
        return 'User(id={}, captured_at={}, created_at={}, user_name={})'.format(self.user_id, self.captured_at,
                                                                                 self.created_at, self.user_name)

    def __str__(self):
        return 'User(id={}, captured_at={}, created_at={}, user_name={})'.format(self.user_id, self.captured_at,
                                                                                 self.created_at, self.user_name)

    def full_str(self):
        user_dict = vars(self)
        user_dict['captured_at'] = self.captured_at.strftime("%m/%d/%Y, %H:%M:%S")
        user_dict['created_at'] = self.created_at.strftime("%m/%d/%Y, %H:%M:%S")
        return json.dumps(user_dict)


class UserBuilder:
    v1_datetime_format = '%a %b %d %H:%M:%S %z %Y'  # example string date: Mon Nov 29 21:18:15 +0000 2010

    @classmethod
    def from_v1_json(cls, user_json: str, captured_at: str) -> User:
        return User(user_id=user_json['id_str'], captured_at=cls.datetime_from_v1_string(captured_at),
                    created_at=cls.datetime_from_v1_string(user_json['created_at']),
                    description=user_json['description'],
                    entities=json.dumps(user_json['entities']),
                    favourites_count=user_json['favourites_count'],
                    followers_count=user_json['followers_count'],
                    following_count=None,
                    friends_count=user_json['friends_count'],
                    listed_count=user_json['listed_count'],
                    name=user_json['name'],
                    pinned_tweet_id=None,
                    profile_image_url=user_json['profile_image_url_https'],
                    protected=user_json['protected'],
                    tweets_count=user_json['statuses_count'],
                    url=user_json['url'],
                    user_name=user_json['screen_name'])

    @classmethod
    def datetime_from_v1_string(cls, datetime_str):
        return datetime.strptime(datetime_str, cls.v1_datetime_format)
