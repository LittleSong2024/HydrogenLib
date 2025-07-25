from abc import ABC, abstractmethod
from io import StringIO


class AbstractSerializer(ABC):
    io = StringIO

    @abstractmethod
    def dump(self, fp, obj):
        ...

    @abstractmethod
    def load(self, fp):
        ...

    def dumps(self, obj):
        io = self.io()
        self.dump(io, obj)
        return io.getvalue()

    def loads(self, string):
        return self.load(self.io(string))
