import pytest
from zadanie_1.databases.database import DatabaseFactory


@pytest.fixture(scope="function", autouse=True)
def connect_to_database(delete_all_tables):
    DatabaseFactory._create_database_object_and_connect()


@pytest.fixture(scope="function", autouse=True)
def disconnect_database(delete_all_tables):
    yield
    DatabaseFactory.get_database_instance().disconnect()


@pytest.fixture(scope="function", autouse=True)
def delete_all_tables():
    DatabaseFactory._create_database_object_and_connect()
    DatabaseFactory.get_database_instance().delete_all_tables()
    yield
    DatabaseFactory.get_database_instance().delete_all_tables()
