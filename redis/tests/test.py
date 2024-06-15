import copy
import time

import pytest
import os
import json
from pytest_check import check
from redis.warehouse.barrel import Barrel
from redis.warehouse.box import Box
from redis.warehouse.warehouse import Warehouse
from redis.databases.mongo_bd import MongoDB
from redis.databases.redis_db import RedisDB
import math


class Test:
    def test_select_all(self):
        assert MongoDB().database.list_collection_names() is not None

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

    def test_read(self):
        _id = MongoDB().insert("box", {"name": "first name"})
        read_data = MongoDB().database["box"].find_one({"_id": _id})
        with check: assert read_data["name"] == "first name"

    def test_read_from_class(self):
        box = Box(1, 2, 3, 4)
        with check: assert box.height == 2

    def test_update(self):
        box = Box(1, 1, 1, 1)
        with check: assert box.height == 1
        box.height = 2
        with check: assert box.height == 2

    def test_delete(self):
        MongoDB().insert("box", {"name": "name"})
        with check: assert MongoDB().database["box"].estimated_document_count() == 1
        MongoDB().delete_docs_from_collection("box")
        with check: assert MongoDB().database["box"].estimated_document_count() == 0

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

    def test_save_to_file(self, delete_files):
        Box(1, 2, 3, 4)
        MongoDB().save_data_to_json_file("box", "testfile")
        files_in_cwd = os.listdir(os.getcwd())
        file_to_load = [file for file in files_in_cwd if file.startswith("testfile_")][0]
        with open(os.path.join(os.getcwd(), file_to_load), "r") as file:
            loaded_data = json.load(file)

        with check: assert loaded_data["_id"] == file_to_load.split("_")[-1].split(".")[0]  # This is id from file name
        with check: assert loaded_data["package_id"] == 1
        with check: assert loaded_data["height"] == 2
        with check: assert loaded_data["width"] == 3
        with check: assert loaded_data["depth"] == 4

    def test_load_from_file(self, delete_files):
        """
        Firstly this test wil create file and then read from it data
        """
        Box(1, 2, 3, 4)
        MongoDB().save_data_to_json_file("box", "testfile")
        files_in_cwd = os.listdir(os.getcwd())
        file_to_load = [file for file in files_in_cwd if file.startswith("testfile_")][0]
        data_from_file = MongoDB().read_from_file(file_to_load)

        with check: assert data_from_file["_id"] == file_to_load.split("_")[-1].split(".")[0]  # This is id from file name
        with check: assert data_from_file["package_id"] == 1
        with check: assert data_from_file["height"] == 2
        with check: assert data_from_file["width"] == 3
        with check: assert data_from_file["depth"] == 4

    def test_redis_add_and_delete(self):
        with check: assert len(RedisDB().get_all_keys()) == 0
        RedisDB().add_to_redis("key", "value")
        with check: assert len(RedisDB().get_all_keys()) == 1
        RedisDB().delete_by_key("key")
        with check: assert len(RedisDB().get_all_keys()) == 0

    def test_redis_add_by_storage(self):
        storage = Warehouse(30)
        box = Box(1, 2, 3, 4)

        with check: assert len(RedisDB().get_all_keys()) == 0
        storage.put(box)
        with check: assert len(RedisDB().get_all_keys()) == 1

    def test_mongodb_if_redis_disconnected(self):
        # Condition
        storage = Warehouse(30)
        box = Box(1, 2, 3, 4)
        storage.put(box)
        all_keys_redis = copy.deepcopy(storage._get_all_keys())

        # Action
        RedisDB().redis_object = None  # There is no longer connection if there is no object ¯\_(ツ)_/¯
        all_keys_mongodb = storage._get_all_keys()

        # Expectation
        with check: assert all_keys_redis == all_keys_mongodb


