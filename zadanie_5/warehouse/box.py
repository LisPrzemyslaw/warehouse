from zadanie_5.warehouse.package import Package
from zadanie_5.databases.mongo_bd import DataBase


class Box(Package):
    def __init__(self, id, height: float, width: float, depth: float):
        super().__init__(id, height * width * depth)
        self.collection = "box"
        self.add_new_object(id, height, width, depth)

        self.__height: float
        self.__width: float
        self.__depth: float

    def add_new_object(self, id, height: float, width: float, depth: float):
        DataBase().insert(self.collection, {"package_id": id, "height": height, "width": width, "depth": depth})

    @property
    def height(self):
        return DataBase().database[self.collection].find_one({"package_id": self.id})["height"]

    @height.setter
    def height(self, value: float):
        DataBase().database[self.collection].update_one({"package_id": self.id}, {"$set": {"height": value}})
        DataBase().database[self.collection_package].update_one({"package_id": self.id}, {"$set": {"package_volume": self.capacity()}})

    @property
    def width(self):
        return DataBase().database[self.collection].find_one({"package_id": self.id})["width"]

    @width.setter
    def width(self, value: float):
        DataBase().database[self.collection].update_one({"package_id": self.id}, {"$set": {"width": value}})
        DataBase().database[self.collection_package].update_one({"package_id": self.id}, {"$set": {"package_volume": self.capacity()}})

    @property
    def depth(self):
        return DataBase().database[self.collection].find_one({"package_id": self.id})["depth"]

    @depth.setter
    def depth(self, value: float):
        DataBase().database[self.collection].update_one({"package_id": self.id}, {"$set": {"depth": value}})
        DataBase().database[self.collection_package].update_one({"package_id": self.id}, {"$set": {"package_volume": self.capacity()}})

    def description(self) -> str:
        pass

    def capacity(self) -> float:
        """
        This method will calculate capacity. it is using properties so it is also geting values from database

        :return: capacity
        """
        return self.height * self.width * self.depth
