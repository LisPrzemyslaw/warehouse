import math

from cassandra.warehouse.package import Package


class Barrel(Package):
    def __init__(self, id: int, radius: float, height: float):
        super().__init__(id, math.pi * radius**2 * height)
        self.collection = "barrel"
        self.add_new_object(id, radius, height)

        self.__radius: float
        self.__height: float

    def add_new_object(self, id: int, radius: float, height: float):
        self._db_object.execute_command(f"""
                                            INSERT INTO warehouse_db.barrel (package_id, radius, height) 
                                            VALUES ({id}, {radius}, {height});
                                            """)

    @property
    def radius(self):
        rows = self._db_object.execute_command(f"SELECT radius from warehouse_db.barrel WHERE package_id = {self.id};")
        return rows[0].radius

    @radius.setter
    def radius(self, value: float):
        self._db_object.execute_command(f"""
                                                UPDATE warehouse_db.barrel
                                                SET radius = {value}
                                                WHERE package_id = {self.id};
                                                """)
        self._db_object.execute_command(f"""
                                        UPDATE package
                                        SET warehouse_db.package_volume = {self.capacity()}
                                        WHERE package_id = {self.id};
                                        """)

    @property
    def height(self):
        rows = self._db_object.execute_command(f"SELECT height from warehouse_db.barrel WHERE package_id = {self.id};")
        return rows[0].height

    @height.setter
    def height(self, value: float):
        self._db_object.execute_command(f"""
                                            UPDATE warehouse_db.barrel
                                            SET height = {value}
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
        return math.pi * self.radius**2 * self.height
