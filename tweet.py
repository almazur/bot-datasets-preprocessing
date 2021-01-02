from datetime import datetime
from twint.tweet import tweet
import json


class Tweet:
    def __init__(self, tweet_id: str, captured_at: datetime, created_at: datetime, user_id: str,
                 timezone: str = None,
                 content: str = None,
                 link: str = None,
                 retweet: bool = None,
                 mentions: list = None,
                 urls: list = None,
                 photos: list = None,
                 video: int = None,
                 lang: str = None,
                 replies_count: int = None,
                 retweets_count: int = None,
                 likes_count: str = None,
                 hashtags: list = None,
                 cashtags: list = None,
                 ):
        self.id = tweet_id
        self.captured_at = captured_at
        self.created_at = created_at
        self.user_id = user_id
        self.timezone = timezone
        self.content = content
        self.link = link
        self.retweet = retweet
        self.mentions = mentions
        self.urls = urls
        self.photos = photos
        self.video = video
        self.lang = lang
        self.replies_count = replies_count
        self.retweets_count = retweets_count
        self.likes_count = likes_count
        self.hashtags = hashtags
        self.cashtags = cashtags

    @property
    def tweet_id(self):
        return self.id

    @property
    def mentions_as_jsons(self):
        return [json.loads(m) for m in self.mentions]

    def __str__(self):
        return 'Tweet(id={}, captured_at={}, created_at={}, user_id={})'.format(self.tweet_id, self.captured_at,
                                                                                self.created_at, self.user_id)

    def __repr__(self):
        return 'Tweet(id={}, captured_at={}, created_at={}, user_id={})'.format(self.tweet_id, self.captured_at,
                                                                                self.created_at, self.user_id)


class TweetBuilder:
    datetime_format = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def from_twint(cls, t: tweet, captured_at: datetime) -> Tweet:
        return Tweet(tweet_id=t.id_str, captured_at=captured_at,
                     created_at=cls.datetime_from_stamps(t.datestamp, t.timestamp),
                     user_id=t.user_id_str,
                     timezone=t.timezone,
                     content=t.tweet,
                     link=t.link,
                     retweet=t.retweet,
                     mentions=[json.dumps(m) for m in t.mentions],
                     urls=t.urls,
                     photos=t.photos,
                     video=t.video,
                     lang=t.lang,
                     replies_count=t.replies_count,
                     retweets_count=t.retweets_count,
                     likes_count=t.likes_count,
                     hashtags=t.hashtags,
                     cashtags=t.cashtags)

    @classmethod
    def datetime_from_stamps(cls, date_str, time_str):
        return datetime.strptime(date_str + ' ' + time_str, cls.datetime_format)
