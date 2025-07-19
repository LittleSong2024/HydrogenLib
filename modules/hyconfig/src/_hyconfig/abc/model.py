from abc import ABC, abstractmethod


class AbstractModel(ABC):
    def __init__(self):
        self.data = None

    @abstractmethod
    def init(self, data):
        ...

    @abstractmethod
    def get(self, name, default=None):
        ...

    @abstractmethod
    def set(self, name, value):
        ...

    @abstractmethod
    def delete(self, name):
        ...

    @abstractmethod
    def exists(self, name):
        ...

    @abstractmethod
    def list(self):
        ...

    def modified(self):
        ...
