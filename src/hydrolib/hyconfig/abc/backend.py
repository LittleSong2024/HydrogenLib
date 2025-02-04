from abc import ABC, abstractmethod
from typing import Iterable, Any, Tuple

from ...file import NeoIo


class ChangeEvent:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class BackendABC(ABC):
    serializer = None

    def __init__(self):
        self.dic = {}
        self.file = None
        self.fd = NeoIo()
        self.fd.create = True

        self._first_loading = True

    @property
    def is_first_loading(self):
        return self._first_loading

    @is_first_loading.setter
    def is_first_loading(self, value):
        self._first_loading = value

    def set_file(self, file):
        self.file = file

    def init(self, **kwargs):
        self.dic = kwargs

    def get(self, key):
        return self.dic.get(key)

    def set(self, key, value):
        self.dic[key] = value
        self.on_change(ChangeEvent(key, value))

    def keys(self) -> Iterable[str]:
        return self.dic.keys()

    def values(self) -> Iterable[Any]:
        return self.dic.values()

    def items(self) -> Iterable[Tuple[str, Any]]:
        return self.dic.items()

    def on_change(self, event: ChangeEvent): ...

    @abstractmethod
    def save(self): ...

    @abstractmethod
    def load(self): ...
