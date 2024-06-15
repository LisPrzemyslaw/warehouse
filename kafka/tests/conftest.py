import pytest
from kafka.databases.mongo_bd import MongoDB
from kafka.databases.kafka_db import TopicCreator
import os


def _delete_all_collections():
    MongoDB().delete_docs_from_collection("barrel")
    MongoDB().delete_docs_from_collection("box")
    MongoDB().delete_docs_from_collection("package")
    MongoDB().delete_docs_from_collection("warehouse")


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
