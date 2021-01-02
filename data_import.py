import sys
import time
import traceback

from cassandra_service import CassandraService
from file_reader import FileReader
from tweet_downloader import TweetDownloader

filename = 'path/to/file'

start = time.time()

db_service = CassandraService()
tweet_downloader = TweetDownloader(min_tweet_count=100, min_tweet_period=100)
file_reader = FileReader()

for u in file_reader.get_users_from_v1_json(filename)[-5:]:
    print('processing user ', u.user_id)
    try:
        tweets = tweet_downloader.download(u.user_id, u.captured_at)
        for t in tweets.all:
            db_service.save_tweet(t)
        db_service.save_user(u)
    except Exception as e:
        print('Encountered error while processing user ', u.user_id)
        user_str = u.full_str()
        exception_str = ''.join(traceback.format_exception(*sys.exc_info()))
        db_service.save_exception({'user': user_str, 'exception': exception_str})

end_t = time.time()
print(end_t - start)
