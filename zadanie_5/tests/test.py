import time

import pytest
import os
import json
from pytest_check import check
import math
from zadanie_5.databases.kafka_db import ConsumerHandler, ProducerHandler
from zadanie_5.warehouse.barrel import Barrel
from zadanie_5.warehouse.box import Box
from zadanie_5.warehouse.warehouse import Warehouse
from zadanie_5.databases.mongo_bd import DataBase


class Test:
    HOST_1 = "localhost:19092"
    HOST_2 = "localhost:29092"
    HOST_3 = "localhost:39092"
    CUSTOMER_1 = "customer_1"
    CUSTOMER_2 = "customer_2"

    def test_created_object(self):
        producer = ProducerHandler(Test.HOST_3)
        consumer_1 = ConsumerHandler(Test.HOST_1, Test.CUSTOMER_1)
        consumer_2 = ConsumerHandler(Test.HOST_2, Test.CUSTOMER_2)
        with check: assert consumer_1 is not None
        with check: assert consumer_2 is not None
        with check: assert producer is not None

    def test_send_message(self):
        producer = ProducerHandler(Test.HOST_3)
        consumer_1 = ConsumerHandler(Test.HOST_1, Test.CUSTOMER_1)
        consumer_2 = ConsumerHandler(Test.HOST_2, Test.CUSTOMER_2)

        producer.send({"id": 12})
        id_1 = consumer_1.receive_data()
        id_2 = consumer_2.receive_data()
        with check: assert id_1 == 12
        with check: assert id_2 is None  # Timeout, no more data

    def test_receive_multiple(self):
        producer = ProducerHandler(Test.HOST_3)
        consumer_1 = ConsumerHandler(Test.HOST_1, Test.CUSTOMER_1)
        consumer_2 = ConsumerHandler(Test.HOST_2, Test.CUSTOMER_2)

        producer.send({"id": 12})
        producer.send({"id": 13})
        id_1 = consumer_1.receive_data()
        id_2 = consumer_2.receive_data()
        with check: assert id_1 == 12
        with check: assert id_2 == 13

    def test_receive_multiple_to_one_consumer(self):
        producer = ProducerHandler(Test.HOST_3)
        consumer_1 = ConsumerHandler(Test.HOST_1, Test.CUSTOMER_1)

        producer.send({"id": 12})
        producer.send({"id": 13})
        id_1 = consumer_1.receive_data()
        id_2 = consumer_1.receive_data()
        with check: assert id_1 == 12
        with check: assert id_2 == 13

    def test_receive_messages(self):
        # setup
        WAREHOUSE_CAPACITY = 500
        box = Box(2342, 1, 2, 3)
        storage = Warehouse(WAREHOUSE_CAPACITY)
        storage.put(box)
        assert storage.get_current_capacity() == WAREHOUSE_CAPACITY - box.capacity()
        producer = ProducerHandler(Test.HOST_3)
        consumer_1 = ConsumerHandler(Test.HOST_1, Test.CUSTOMER_1)
        consumer_2 = ConsumerHandler(Test.HOST_2, Test.CUSTOMER_2)

        # action
        producer.send({"id": 2342})
        customer_1_id = consumer_1.receive_data()
        customer_2_id = consumer_2.receive_data()

        # Expectation 1
        assert customer_1_id is not None
        storage.take_out(customer_1_id)
        assert storage.get_current_capacity() == WAREHOUSE_CAPACITY
        # Expectation 2
        assert customer_2_id is None
        assert storage.take_out(customer_1_id) is False  # returns false if not taken

    #####################
    # UNIT TESTS
    #####################
    def test_select_all(self):
        assert DataBase().database.list_collection_names() is not None

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
        _id = DataBase().insert("box", {"name": "first name"})
        read_data = DataBase().database["box"].find_one({"_id": _id})
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
        DataBase().insert("box", {"name": "name"})
        with check: assert DataBase().database["box"].estimated_document_count() == 1
        DataBase().delete_docs_from_collection("box")
        with check: assert DataBase().database["box"].estimated_document_count() == 0

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
        DataBase().save_data_to_json_file("box", "testfile")
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
        DataBase().save_data_to_json_file("box", "testfile")
        files_in_cwd = os.listdir(os.getcwd())
        file_to_load = [file for file in files_in_cwd if file.startswith("testfile_")][0]
        data_from_file = DataBase().read_from_file(file_to_load)

        with check: assert data_from_file["_id"] == file_to_load.split("_")[-1].split(".")[0]  # This is id from file name
        with check: assert data_from_file["package_id"] == 1
        with check: assert data_from_file["height"] == 2
        with check: assert data_from_file["width"] == 3
        with check: assert data_from_file["depth"] == 4
