import pytest
from pytest_check import check
from cassandra.warehouse.barrel import Barrel
from cassandra.warehouse.box import Box
from cassandra.warehouse.warehouse import Warehouse
from cassandra.databases.cassandra_db import CassandraFactory
import math


class Test:
    def test_select_all(self):
        cdb = CassandraFactory.get_database_instance()
        cdb.create_default_tables()
        rows = cdb.execute_command("SELECT * FROM warehouse_db.box;")

    def test_create(self):
        box = Box(2342, 1, 2, 3)
        with check: assert box.id == 2342
        with check: assert box.height == 1
        with check: assert box.width == 2
        with check: assert box.depth == 3

        barrel = Barrel(9391, 4, 5)
        with check: assert barrel.id == 9391
        with check: assert barrel.radius == 4
        with check: assert barrel.height == 5

        storage = Warehouse(400)
        with check: assert storage.get_current_capacity() == 400

    def test_read_from_class(self):
        box = Box(1, 2, 3, 4)
        with check: assert box.height == 2

    def test_update(self):
        box = Box(1, 1, 1, 1)
        with check: assert box.height == 1
        box.height = 2
        with check: assert box.height == 2

    def test_delete(self):
        cdb = CassandraFactory.get_database_instance()
        cdb.execute_command("INSERT INTO warehouse_db.box (package_id, height, width, depth) VALUES (1, 1, 1, 1)")
        rows = cdb.execute_command("SELECT package_id FROM warehouse_db.box")

        counter = 0
        for row in rows:
            print(row.package_id)
            counter += 1
        with check: assert counter == 1
        cdb.execute_command("TRUNCATE warehouse_db.box")
        rows = cdb.execute_command("SELECT package_id FROM warehouse_db.box")
        counter = 0
        for row in rows:
            counter += 1
        with check: assert counter == 0

    def test_capacity(self):
        box = Box(2342, 1, 2, 3)
        with check: assert box.capacity() == 6

        barrel = Barrel(9391, 4, 5)
        with check: assert barrel.capacity() == math.pi * 4 ** 2 * 5

    def test_store_items(self):
        box = Box(2342, 1, 2, 3)
        barrel = Barrel(9391, 4, 5)
        storage = Warehouse(30)

        with check: assert storage.get_current_capacity() == 30
        storage.put(box)
        with check: assert storage.get_current_capacity() == 24
        with check: assert storage.get_number_of_items_in_storage() == 1
        with pytest.raises(ValueError):
            storage.put(barrel)  # this statement checks if errors occur (barrel > max_capacity)
        with check: assert storage.get_current_capacity() == 24  # if not putted, then not change capacity
        with check: assert storage.get_number_of_items_in_storage() == 1
