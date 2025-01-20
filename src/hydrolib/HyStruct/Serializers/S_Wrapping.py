from types import FunctionType

from . import Serializer


class Wrapping(Serializer):
    def __init__(self, dumps: FunctionType, loads: FunctionType):
        self._dumps = dumps
        self._loads = loads

    def dumps(self, obj):
        return self._dumps(obj)

    def loads(self, obj):
        return self._loads(obj)
