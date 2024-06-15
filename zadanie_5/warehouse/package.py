from abc import ABC, abstractmethod
from zadanie_5.databases.mongo_bd import DataBase


class Package(ABC):
    def __init__(self, id: int, capacity: float):
        self.package_id: int = id
        self.collection_package = "package"
        self.set_id_object(id, capacity)

    def __dict__(self):
        return {"package_id": self.package_id, "package_volume": self.get_package_volume()}

    def set_id_object(self, id, capacity):
        DataBase().insert(self.collection_package, {"package_id": id, "package_volume": capacity})

    @property
    def id(self):
        return DataBase().database[self.collection_package].find_one({"package_id": self.package_id})["package_id"]

    def get_package_volume(self):
        return DataBase().database[self.collection_package].find_one({"package_id": self.package_id})["package_volume"]

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def capacity(self) -> float:
        pass
