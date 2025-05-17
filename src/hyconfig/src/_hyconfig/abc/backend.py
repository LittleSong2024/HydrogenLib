from abc import ABC, abstractmethod
from typing import Iterable, Any, Tuple

from ..._hycore.file import NeoIO


class ChangeEvent:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class AbstractBackend(ABC):
    serializer = None
    support_types = None

    def __init_subclass__(cls, **kwargs):
        if cls.serializer is None:
            raise TypeError("BackendABC subclass must have a serializer attribute.")
        if cls.support_types is None:
            raise TypeError("BackendABC subclass must have a support_types attribute.")

    def __init__(self):
        self.file = None
        self.existing = False

        self._data = {}
        self._io = NeoIO()
        self._io.create = True

    def _support_1(self, type):
        return type in self.support_types

    def _support_2(self, type):
        for i in self.support_types:
            if issubclass(type, i):
                return True
        return False

    def support(self, type):
        return self._support_1(type) or self._support_2(type)

    def init(self, **kwargs):
        self._data = kwargs

    def get(self, key):
        return self._data.get(key)

    def set(self, key, value):
        self._data[key] = value
        self.on_change(ChangeEvent(key, value))

    def keys(self) -> Iterable[str]:
        return self._data.keys()

    def values(self) -> Iterable[Any]:
        return self._data.values()

    def items(self) -> Iterable[Tuple[str, Any]]:
        return self._data.items()

    def on_change(self, event: ChangeEvent):
        ...

    @abstractmethod
    def save(self):
        ...

    @abstractmethod
    def load(self):
        ...
