import math

from kafka.warehouse.package import Package
from kafka.databases.mongo_bd import MongoDB


class Barrel(Package):
    def __init__(self, id: int, radius: float, height: float):
        super().__init__(id, math.pi * radius**2 * height)
        self.collection = "barrel"
        self.add_new_object(id, radius, height)

        self.__radius: float
        self.__height: float

    def add_new_object(self, id: int, radius: float, height: float):
        MongoDB().insert(self.collection, {"package_id": id, "radius": radius, "height": height})

    @property
    def radius(self):
        return MongoDB().database[self.collection].find_one({"package_id": self.id})["radius"]

    @radius.setter
    def radius(self, value: float):
        MongoDB().database[self.collection].update_one({"package_id": self.id}, {"$set": {"radius": value}})
        MongoDB().database[self.collection_package].update_one({"package_id": self.id}, {"$set": {"package_volume": self.capacity()}})

    @property
    def height(self):
        return MongoDB().database[self.collection].find_one({"package_id": self.id})["height"]

    @height.setter
    def height(self, value: float):
        MongoDB().database[self.collection].update_one({"package_id": self.id}, {"$set": {"height": value}})
        MongoDB().database[self.collection_package].update_one({"package_id": self.id}, {"$set": {"package_volume": self.capacity()}})

    def description(self) -> str:
        pass

    def capacity(self) -> float:
        return math.pi * self.radius**2 * self.height
