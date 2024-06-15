import pytest
from zadanie_5.databases.mongo_bd import DataBase
from zadanie_5.databases.kafka_db import TopicCreator
import os


def _delete_all_collections():
    DataBase().delete_docs_from_collection("barrel")
    DataBase().delete_docs_from_collection("box")
    DataBase().delete_docs_from_collection("package")
    DataBase().delete_docs_from_collection("warehouse")


@pytest.fixture(scope="function", autouse=True)
def delete_all_data():
    _delete_all_collections()
    yield
    _delete_all_collections()


@pytest.fixture(scope="function", autouse=False)
def delete_files():
    yield
    all_files = os.listdir(os.getcwd())
    files_to_delete = [file for file in all_files if file.endswith(".json")]
    for file in files_to_delete:
        os.remove(os.path.join(os.getcwd(), file))


@pytest.fixture(scope="session", autouse=True)
def create_topic():
    TopicCreator()
