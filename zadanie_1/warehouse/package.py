from abc import ABC, abstractmethod
from zadanie_1.databases.database import DatabaseFactory


class Package(ABC):
    def __init__(self, id: int, capacity: float):
        self._db_object = DatabaseFactory.get_database_instance()
        self.set_id_object(id, capacity)
        self.package_id: int = id
        self.collection = "package"

    def set_id_object(self, id, capacity):
        self._db_object.cursor.execute(f"""
                                            INSERT INTO package (package_id, package_volume) 
                                            VALUES ({id}, {capacity}); 
                                            """)
        self._db_object.connection.commit()
    @property
    def id(self):
        self._db_object.cursor.execute(f"SELECT package_id from Package WHERE package_id = {self.package_id};")
        return self._db_object.cursor.fetchone()[0]

    def get_package_volume(self):
        self._db_object.cursor.execute(f"SELECT package_volume from Package WHERE package_id = {self.package_id};")
        return self._db_object.cursor.fetchone()[0]

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def capacity(self) -> float:
        pass
