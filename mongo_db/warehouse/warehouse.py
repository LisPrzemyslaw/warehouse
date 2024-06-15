from mongo_db.warehouse.package import Package
from mongo_db.databases.mongo_bd import MongoDB


class Warehouse:
    def __init__(self, capacity):
        self.collection = "warehouse"
        self.collection_package = "package"
        self.max_capacity: float = capacity

    def put(self, package: Package):
        if self.get_current_capacity() - package.capacity() < 0:
            raise ValueError("Package not fitted into storage!")
        MongoDB().insert(self.collection, {"package_id": package.package_id})

    def get_number_of_items_in_storage(self) -> int:
        return int(MongoDB().database[self.collection].estimated_document_count())

    def get_volume_of_storage(self) -> float:
        packages_ids = [data.get("package_id") for data in MongoDB().database[self.collection].find()]
        volume = sum([float(data["package_volume"]) for data in MongoDB().database[self.collection_package].find() if data["package_id"] in packages_ids])
        return float(volume)

    def get_current_capacity(self) -> float:
        return self.max_capacity - self.get_volume_of_storage()

    def package(self, index: int) -> Package:
        ...

    def description(self) -> str:
        ...
