from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def connect(self):
        pass

