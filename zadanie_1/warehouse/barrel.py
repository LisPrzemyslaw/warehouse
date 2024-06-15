from zadanie_1.warehouse.package import Package
import math


class Barrel(Package):
    def __init__(self, id: int, radius: float, height: float):
        super().__init__(id, math.pi * radius**2 * height)
        self.add_new_object(id, radius, height)

    def add_new_object(self, id: int, radius: float, height: float):
        self._db_object.cursor.execute(f"""
                                            INSERT INTO barrel (package_id, radius, height) 
                                            VALUES ({id}, {radius}, {height});
                                            """)
        self._db_object.connection.commit()

    @property
    def radius(self):
        self._db_object.cursor.execute(f"SELECT barrel.radius from barrel WHERE barrel.package_id = {self.id}")
        return self._db_object.cursor.fetchone()[0]

    @radius.setter
    def radius(self, value: float):
        self._db_object.cursor.execute(f"""
                                                UPDATE barrel
                                                SET radius = {value}
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
    def height(self):
        self._db_object.cursor.execute(f"SELECT barrel.height from barrel WHERE barrel.package_id = {self.id}")
        return self._db_object.cursor.fetchone()[0]

    @height.setter
    def height(self, value: float):
        self._db_object.cursor.execute(f"""
                                            UPDATE barrel
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

    def description(self) -> str:
        pass

    def capacity(self) -> float:
        return math.pi * self.radius**2 * self.height
