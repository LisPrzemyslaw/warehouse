from cassandra.cluster import Cluster


class CassandraDB:
    def __init__(self):
        self.cluster = Cluster(['127.0.0.1'], port=9042)
        self.session = self.cluster.connect('warehouse_db', wait_for_all_pools=True)
        print("Connected to Cassandra DB")
        # self.session.execute()
        # LOCAL_ONE

    def create_default_tables(self):
        self.session.execute("""CREATE TABLE IF NOT EXISTS warehouse_db.Package (
                                        package_id int primary key,
                                        package_volume float
                                );
                            """)
        self.session.execute("""CREATE TABLE IF NOT EXISTS warehouse_db.Warehouse (packages_id int primary key);""")

        self.session.execute("""CREATE TABLE IF NOT EXISTS warehouse_db.Box (
                                        package_id int primary key,
                                        height float,
                                        width float,
                                        depth float
                                );
                            """)

        self.session.execute("""CREATE TABLE IF NOT EXISTS warehouse_db.Barrel (
                                        package_id int primary key,
                                        radius float,
                                        height float
                                );
                            """)

    def delete_all(self):
        self.session.execute("""TRUNCATE warehouse_db.Package;""")
        self.session.execute("""TRUNCATE warehouse_db.Warehouse;""")
        self.session.execute("""TRUNCATE warehouse_db.Box;""")
        self.session.execute("""TRUNCATE warehouse_db.Barrel;""")

    def execute_command(self, command):
        return self.session.execute(command)


class CassandraFactory:
    _DATABASE: CassandraDB = None

    @staticmethod
    def _create_database_object_and_connect():
        if CassandraFactory._DATABASE is None:
            CassandraFactory._DATABASE = CassandraDB()
        CassandraFactory._DATABASE.create_default_tables()

    @staticmethod
    def get_database_instance():
        if CassandraFactory._DATABASE is None:
            CassandraFactory._create_database_object_and_connect()
        return CassandraFactory._DATABASE


if __name__ == '__main__':
    cdb = CassandraFactory.get_database_instance()
    cdb.create_default_tables()
    rows = cdb.execute_command("SELECT * FROM warehouse_db.box;")
