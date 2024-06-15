from warehouse.databases.database_interface import DatabaseInterface
from warehouse.databases.postgres_db import PostgresDB


class DatabaseFactory:
    _DATABASE: DatabaseInterface = None

    _AVAILABLE_DATABASES = {"POSTGRES": PostgresDB}

    @staticmethod
    def _create_database_object_and_connect(database_type: str):
        if DatabaseFactory._DATABASE is None:
            DatabaseFactory._DATABASE = DatabaseInterface._AVAILABLE_DATABASES[database_type]()
        DatabaseFactory._DATABASE.connect()
        DatabaseFactory._DATABASE.create_default_tables()

    @staticmethod
    def get_database_instance():
        if DatabaseFactory._DATABASE is None:
            raise Exception("Database object has not been created.")
        return DatabaseFactory._DATABASE