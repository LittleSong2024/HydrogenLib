from ..abc.model import *


class DefaultModel(AbstractModel):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.changes = set()

    def init(self, data):
        self.data = data

    def set(self, name, value):
        if self.data.get(name) != value:
            self.changes.add(name)
        self.data[name] = value

    def get(self, name, default=None):
        return self.data.get(name, default)

    def delete(self, name):
        del self.data[name]
        self.changes.add(name)

    def exists(self, name):
        return name in self.data

    def list(self):
        return list(self.data.keys())

    def modified(self):
        ch = self.changes
        self.changes = set()
        return ch
