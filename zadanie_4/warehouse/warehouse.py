from zadanie_4.warehouse.package import Package
from zadanie_4.databases.cassandra_db import CassandraFactory


class Warehouse:
    def __init__(self, capacity):
        self._db_object = CassandraFactory.get_database_instance()
        self.max_capacity: float = capacity

    def put(self, package: Package):
        if self.get_current_capacity() - package.capacity() < 0:
            raise ValueError("Package not fitted into storage!")
        self._db_object.execute_command(f"""
                                        INSERT INTO warehouse_db.warehouse (packages_id) 
                                        VALUES ({package.package_id}); 
                                        """)

    def get_number_of_items_in_storage(self) -> int:
        rows = self._db_object.execute_command(f"SELECT COUNT(packages_id) AS number from warehouse_db.warehouse;")
        return int(rows[0].number)

    def get_volume_of_storage(self) -> float:
        all_packages_ids = [row.packages_id for row in self._db_object.execute_command("SELECT packages_id FROM warehouse_db.warehouse")]
        volume = 0
        for package_id in all_packages_ids:
            rows = self._db_object.execute_command(f"SELECT package_volume FROM warehouse_db.package WHERE package_id = {package_id};")
            volume += rows[0].package_volume
        return float(volume)

    def get_current_capacity(self) -> float:
        return self.max_capacity - self.get_volume_of_storage()

    def package(self, index: int) -> Package:
        ...

    def description(self) -> str:
        ...
