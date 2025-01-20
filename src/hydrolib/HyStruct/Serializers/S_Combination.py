from typing import Any

from . import Serializer


class Combination(Serializer):
    """
    Combination of multiple serializers
    """
    def __init__(self, *args: Serializer):
        self._serializers = list(args)

    def append(self, serializer: Serializer):
        self._serializers.append(serializer)

    def extend(self, serializers: list[Serializer]):
        self._serializers.extend(serializers)

    def clear(self):
        self._serializers.clear()

    def set(self, serializers: list[Serializer]):
        self._serializers = serializers

    def index_at(self, __i):
        return self._serializers[__i]

    def pop(self, __i):
        return self._serializers.pop(__i)

    def dumps(self, data) -> bytes:
        for serializer in self._serializers:
            data = serializer.dumps(data)
        return data

    def loads(self, data) -> Any:
        for serializer in reversed(self._serializers):
            data = serializer.loads(data)
        return data
