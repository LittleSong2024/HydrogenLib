from abc import ABC, abstractmethod
from typing import Iterable, Any, Tuple

from ...file import NeoIo


class ChangeEvent:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class BackendABC(ABC):
    serializer = None

    def __init__(self, parent=None):
        self.defaults = {}
        self.dic = {}
        self.file = None
        self.fd = NeoIo()
        self.fd.create = True
        self.parent = parent

        self._first_loading = True

    @property
    def is_first_loading(self):
        return self._first_loading

    @is_first_loading.setter
    def is_first_loading(self, value):
        self._first_loading = value

    def set_file(self, file):
        self.file = file

    def set_defaults(self, **kwargs) -> None:
        self.defaults = kwargs

    def init(self, **kwargs):
        self.dic = kwargs

    def get(self, key):
        return self.dic.get(key, self.defaults.get(key))

    def set(self, key, value):
        self.dic[key] = value
        self.changeEvent(ChangeEvent(key, value))

    def keys(self) -> Iterable[str]:
        return self.dic.keys()

    def values(self) -> Iterable[Any]:
        return self.dic.values()

    def items(self) -> Iterable[Tuple[str, Any]]:
        return self.dic.items()

    def changeEvent(self, event: ChangeEvent): ...

    @abstractmethod
    def save(self): ...

    @abstractmethod
    def load(self): ...
