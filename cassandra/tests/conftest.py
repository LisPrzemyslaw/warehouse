import pytest
from cassandra.databases.cassandra_db import CassandraFactory


@pytest.fixture(scope="function", autouse=True)
def delete_all_data():
    CassandraFactory.get_database_instance().delete_all()
    CassandraFactory.get_database_instance().create_default_tables()
    yield
    CassandraFactory.get_database_instance().delete_all()
