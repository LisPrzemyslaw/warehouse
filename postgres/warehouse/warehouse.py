from postgres.warehouse.package import Package
from postgres.databases.postgresdb import DatabaseFactory


class Warehouse:
    def __init__(self, capacity):
        self._db_object = DatabaseFactory.get_database_instance()
        self.max_capacity: float = capacity

    def put(self, package: Package):
        # TODO IF NOT EXIST
        # INSERT INTO package (package_id, package_volume)
        # VALUES({package.package_id}, {package.capacity()});
        if self.get_current_capacity() - package.capacity() < 0:
            raise ValueError("Package not fitted into storage!")
        self._db_object.cursor.execute(f"""
                                            INSERT INTO warehouse (packages_id) 
                                            VALUES ({package.package_id}); 
                                            """)
        self._db_object.connection.commit()

    # def get_id_by_index(self, index: int) -> int:
    #     self._db_object.cursor.execute(f"SELECT packages_id from warehouse;")
    #     return int(self._db_object.cursor.fetchone()[0])

    def get_number_of_items_in_storage(self) -> int:
        self._db_object.cursor.execute(f"SELECT COUNT(packages_id) from warehouse;")
        return int(self._db_object.cursor.fetchone()[0])

    def get_volume_of_storage(self) -> float:
        self._db_object.cursor.execute(
            f"SELECT COALESCE(sum(package.package_volume), 0) from warehouse JOIN package on package.package_id = warehouse.packages_id;")
        return float(self._db_object.cursor.fetchone()[0])

    def get_current_capacity(self) -> float:
        return self.max_capacity - self.get_volume_of_storage()

    def package(self, index: int) -> Package:
        ...

    def description(self) -> str:
        ...
