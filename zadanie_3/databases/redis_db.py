from __future__ import annotations

from typing import Union

import redis
from dotenv import load_dotenv
import os


class RedisDB:
    __instance: RedisDB = None

    def __new__(cls, *args, **kwargs):
        if RedisDB.__instance is None:
            RedisDB.__instance = object.__new__(cls)
            RedisDB.initialized = None
        return RedisDB.__instance

    def __init__(self):
        if self.initialized is None:
            load_dotenv()
            self.redis_object = redis.Redis(host=os.getenv("REDIS_HOST"),
                                            port=int(os.getenv("REDIS_PORT")),
                                            password=os.getenv("REDIS_PASSWORD"),
                                            ssl=True)
            self.initialized = True

    def add_to_redis(self, key, value):
        self.redis_object.set(key, value)

    def get(self, name):
        return self.redis_object.get(name)

    def get_all_keys(self):
        return self.redis_object.keys()

    def delete_by_key(self, key='*'):
        """
        This function is deleting by key
        :param key: by default delete all keys
        :return:
        """
        try:
            keys = self.redis_object.keys(key)
            self.redis_object.delete(*keys)
        except redis.exceptions.ResponseError:
            print(f"key: {key} does not exist!")
        except AttributeError:
            # This statement can occur with test when we deleted redis
            pass


if __name__ == '__main__':
    pass