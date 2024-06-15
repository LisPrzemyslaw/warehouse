import psycopg2


class DataBase:
    def __init__(self):
        self.__db_name = "nbddb"
        self.__user = "nbd"
        self.__password = "nbdpassword"

        self.connection = None
        self.cursor = None

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.connection = psycopg2.connect(f"dbname={self.__db_name} user={self.__user} password={self.__password}")
            print(f"Connected to database: {self.__db_name}")
            # create a cursor
            self.cursor = self.connection.cursor()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def disconnect(self):
        self.cursor.close()
        self.connection.close()
        print(f"Database: {self.__db_name} disconnected.")

    def create_default_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Package (
                                        package_id int primary key,
                                        package_volume float
                                
                                );
                                CREATE TABLE IF NOT EXISTS Warehouse (
                                        packages_id int primary key,
                                        FOREIGN KEY (packages_id) REFERENCES  Package (package_id)
                                );
                                
                                CREATE TABLE IF NOT EXISTS Box (
                                        package_id int primary key,
                                        height float,
                                        width float,
                                        depth float,
                                        FOREIGN KEY (package_id) REFERENCES  Package (package_id)
                                );
                                CREATE TABLE IF NOT EXISTS Barrel (
                                        package_id int primary key,
                                        radius float,
                                        height float,
                                        FOREIGN KEY (package_id) REFERENCES  Package (package_id)
                                );""")
        self.connection.commit()

    def delete_all_tables(self):
        self.connect()
        self.cursor.execute("""
                            DROP TABLE IF EXISTS Package CASCADE;
                            DROP TABLE IF EXISTS Warehouse CASCADE;
                            DROP TABLE IF EXISTS Box CASCADE;
                            DROP TABLE IF EXISTS Barrel CASCADE;""")
        self.connection.commit()


class DatabaseFactory:
    _DATABASE: DataBase = None

    @staticmethod
    def _create_database_object_and_connect():
        if DatabaseFactory._DATABASE is None:
            DatabaseFactory._DATABASE = DataBase()
        DatabaseFactory._DATABASE.connect()
        DatabaseFactory._DATABASE.create_default_tables()


    @staticmethod
    def get_database_instance():
        return DatabaseFactory._DATABASE


if __name__ == '__main__':
    DatabaseFactory._create_database_object_and_connect()

    #############################################
    # TESTING PURPOSE
    #############################################

    # db = DatabaseFactory.get_database_instance()
    # db.delete_all_tables()
    # db.cursor.execute(""" INSERT INTO package(package_id) VALUES (2);""")
    # db.connection.commit()
    # db.cursor.execute(""" INSERT INTO package(package_id) VALUES (3);""")
    # db.connection.commit()
                          # INSERT INTO package(package_id) VALUES (2);
                          #   INSERT INTO box (package_id, height, width, depth)
                          #                   VALUES (1, 2, 3, 4);""")
    # db.cursor.execute('SELECT * from package where package_id = 2')
    #
    #
    # print(db.cursor.fetchone())
    # db.cursor.execute("select * from box")
    # data = db.cursor.fetchone()
    # print(data)
    # DatabaseFactory.get_database_instance().disconnect()
