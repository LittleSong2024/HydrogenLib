from types import FunctionType
from typing import Any

from . import AbstractSerializer


class Wrapping(AbstractSerializer):
    def __init__(self, dumps: FunctionType = None, loads: FunctionType = None, dump: FunctionType = None, load: FunctionType = None):
        self._dumps = dumps
        self._loads = loads
        self._load = load
        self._dump = dump

    def dump(self, fp) -> None:
        return self._dump(fp)

    def load(self, fp) -> Any:
        return self._load(fp)

    def dumps(self, obj):
        return self._dumps(obj)

    def loads(self, obj):
        return self._loads(obj)
