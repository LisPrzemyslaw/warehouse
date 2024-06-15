import pytest
from pytest_check import check
from zadanie_1.warehouse.barrel import Barrel
from zadanie_1.warehouse.box import Box
from zadanie_1.warehouse.warehouse import Warehouse
from zadanie_1.databases.database import DatabaseFactory
import math


class Test:
    def test_select_all(self):
        DatabaseFactory.get_database_instance().cursor.execute("SELECT * FROM box")

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

        # with check: assert storage.get_id_by_index(0) == 2342
