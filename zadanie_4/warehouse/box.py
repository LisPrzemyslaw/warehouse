from zadanie_4.warehouse.package import Package


class Box(Package):
    def __init__(self, id, height: float, width: float, depth: float):
        super().__init__(id, height * width * depth)
        self.add_new_object(id, height, width, depth)

        self.__height: float
        self.__width: float
        self.__depth: float

    def add_new_object(self, id, height: float, width: float, depth: float):
        self._db_object.execute_command(f"""
                                        INSERT INTO warehouse_db.box (package_id, height, width, depth) 
                                        VALUES ({id}, {height}, {width}, {depth});
                                        """)

    @property
    def height(self):
        rows = self._db_object.execute_command(f"SELECT height from warehouse_db.box WHERE package_id = {self.id};")
        return rows[0].height

    @height.setter
    def height(self, value: float):
        self._db_object.execute_command(f"""
                                        UPDATE warehouse_db.box
                                        SET height = {value}
                                        WHERE package_id = {self.id};
                                        """)
        self._db_object.execute_command(f"""
                                        UPDATE warehouse_db.package
                                        SET package_volume = {self.capacity()}
                                        WHERE package_id = {self.id};
                                        """)

    @property
    def width(self):
        rows = self._db_object.execute_command(f"SELECT width from warehouse_db.box WHERE package_id = {self.id};")
        return rows[0].width

    @width.setter
    def width(self, value: float):
        self._db_object.execute_command(f"""
                                        UPDATE warehouse_db.box
                                        SET width = {value}
                                        WHERE package_id = {self.id};
                                        """)
        self._db_object.execute_command(f"""
                                        UPDATE warehouse_db.package
                                        SET package_volume = {self.capacity()}
                                        WHERE package_id = {self.id};
                                        """)

    @property
    def depth(self):
        rows = self._db_object.execute_command(f"SELECT depth from warehouse_db.box WHERE package_id = {self.id}")
        return rows[0].depth

    @depth.setter
    def depth(self, value: float):
        self._db_object.execute_command(f"""
                                        UPDATE warehouse_db.box
                                        SET depth = {value}
                                        WHERE package_id = {self.id};
                                        """)
        self._db_object.execute_command(f"""
                                        UPDATE warehouse_db.package
                                        SET package_volume = {self.capacity()}
                                        WHERE package_id = {self.id};
                                        """)

    def description(self) -> str:
        pass

    def capacity(self) -> float:
        """
        This method will calculate capacity. it is using properties so it is also geting values from database

        :return: capacity
        """
        return self.height * self.width * self.depth
