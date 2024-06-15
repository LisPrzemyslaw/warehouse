import time

from redis.warehouse.package import Package
from redis.databases.mongo_bd import MongoDB
from redis.databases.redis_db import RedisDB


def get_in_loop(func):
    def wrapper(self, *args, **kwargs):
        counter = 0
        while counter < 3:
            try:
                return func(self, *args, **kwargs)
            except:
                counter += 1
        return [data["package_id"] for data in MongoDB().database[self.collection].find({})]
    return wrapper


class Warehouse:
    def __init__(self, capacity):
        self.collection = "warehouse"
        self.collection_package = "package"
        self.max_capacity: float = capacity

    def put(self, package: Package):
        if self.get_current_capacity() - package.capacity() < 0:
            raise ValueError("Package not fitted into storage!")
        RedisDB().add_to_redis(package.package_id, "package_id")
        MongoDB().insert(self.collection, {"package_id": package.package_id})

    @get_in_loop
    def _get_all_keys(self):
        return [int(key) for key in RedisDB().redis_object.keys()]

    def get_number_of_items_in_storage(self) -> int:
        return len(self._get_all_keys())

    def get_volume_of_storage(self) -> float:
        packages_ids = [int(key) for key in self._get_all_keys()]
        volume = sum([float(data["package_volume"]) for data in MongoDB().database[self.collection_package].find() if data["package_id"] in packages_ids])
        return float(volume)

    def get_current_capacity(self) -> float:
        return self.max_capacity - self.get_volume_of_storage()

    def package(self, index: int) -> Package:
        ...

    def description(self) -> str:
        ...
