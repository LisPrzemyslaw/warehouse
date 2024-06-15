from postgres.warehouse.package import Package


class Box(Package):
    def __init__(self, id, height: float, width: float, depth: float):
        super().__init__(id, height * width * depth)
        self.add_new_object(id, height, width, depth)

        self.__height: float
        self.__width: float
        self.__depth: float

    def add_new_object(self, id, height: float, width: float, depth: float):
        self._db_object.cursor.execute(f"""
                                            INSERT INTO box (package_id, height, width, depth) 
                                            VALUES ({id}, {height}, {width}, {depth});
                                            """)
        self._db_object.connection.commit()

    @property
    def height(self):
        self._db_object.cursor.execute(f"SELECT box.height from box WHERE box.package_id = {self.id}")
        return self._db_object.cursor.fetchone()[0]

    @height.setter
    def height(self, value: float):
        self._db_object.cursor.execute(f"""
                                        UPDATE box
                                        SET height = {value}
                                        WHERE package_id = {self.id};
                                        """)
        self._db_object.connection.commit()
        self._db_object.cursor.execute(f"""
                                        UPDATE package
                                        SET package_volume = {self.capacity()}
                                        WHERE package_id = {self.id};
                                        """)
        self._db_object.connection.commit()

    @property
    def width(self):
        self._db_object.cursor.execute(f"SELECT box.width from box WHERE box.package_id = {self.id}")
        return self._db_object.cursor.fetchone()[0]

    @width.setter
    def width(self, value: float):
        self._db_object.cursor.execute(f"""
                                            UPDATE box
                                            SET width = {value}
                                            WHERE package_id = {self.id};
                                            """)
        self._db_object.connection.commit()
        self._db_object.cursor.execute(f"""
                                        UPDATE package
                                        SET package_volume = {self.capacity()}
                                        WHERE package_id = {self.id};
                                        """)
        self._db_object.connection.commit()

    @property
    def depth(self):
        self._db_object.cursor.execute(f"SELECT box.depth from box WHERE box.package_id = {self.id}")
        return self._db_object.cursor.fetchone()[0]

    @depth.setter
    def depth(self, value: float):
        self._db_object.cursor.execute(f"""
                                            UPDATE box
                                            SET depth = {value}
                                            WHERE package_id = {self.id};
                                            """)
        self._db_object.connection.commit()
        self._db_object.cursor.execute(f"""
                                        UPDATE package
                                        SET package_volume = {self.capacity()}
                                        WHERE package_id = {self.id};
                                        """)
        self._db_object.connection.commit()

    def description(self) -> str:
        pass

    def capacity(self) -> float:
        """
        This method will calculate capacity. it is using properties so it is also geting values from database

        :return: capacity
        """
        return self.height * self.width * self.depth
