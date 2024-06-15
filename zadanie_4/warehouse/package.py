from abc import ABC, abstractmethod
from zadanie_4.databases.cassandra_db import CassandraFactory


class Package(ABC):
    def __init__(self, id: int, capacity: float):
        self._db_object = CassandraFactory.get_database_instance()
        self.set_id_object(id, capacity)
        self.package_id: int = id
        self.collection = "package"

    def set_id_object(self, id, capacity):
        self._db_object.execute_command(f"""
                                        INSERT INTO warehouse_db.package (package_id, package_volume) 
                                        VALUES ({id}, {capacity}); 
                                        """)

    @property
    def id(self):
        rows = self._db_object.execute_command(f"SELECT package_id from warehouse_db.Package WHERE package_id = {self.package_id};")
        return rows[0].package_id

    def get_package_volume(self):
        rows = self._db_object.execute_command(f"SELECT package_volume from warehouse_db.Package WHERE package_id = {self.package_id};")
        return rows[0].package_volume

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def capacity(self) -> float:
        pass
