import json
from cassandra.cluster import Cluster
from user import UserBuilder


def get_users_from_v1_json(filename):
    with open(filename, encoding='utf-8') as f:
        js = json.load(f)
        users = [UserBuilder.from_v1_json(j['user'], j['created_at']) for j in js]
    return users


def connect(keyspace='data'):
    cluster = Cluster()
    return cluster.connect(keyspace)


def prepare_insert_statement(session):
    return session.prepare(
        """
        INSERT INTO pronbots_2019 (id, captured_at, created_at, description, entities, favourites_count, followers_count,
            following_count, friends_count, listed_count, name, pinned_tweet_id, profile_image_url, protected,
            tweets_count, url, user_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
    )


def save_user(session, insert_stmt, user):
    session.execute(insert_stmt, vars(user))


filename = 'path/to/file'
# table_name = 'pronbots_2019'

import time
start = time.time()

session = connect()
user_insert_stmt = prepare_insert_statement(session)
for u in get_users_from_v1_json(filename)[1:]:
    save_user(session, user_insert_stmt, u)

end_t = time.time()

print(end_t - start)
