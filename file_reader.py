import json

from user import UserBuilder


class FileReader:

    @staticmethod
    def get_users_from_v1_json(filename):
        with open(filename, encoding='utf-8') as f:
            js = json.load(f)
            users = [UserBuilder.from_v1_json(j['user'], j['created_at']) for j in js]
        return users
