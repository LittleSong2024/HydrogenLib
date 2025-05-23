from abc import ABCMeta

from ..abstract import AbstractMarker, restore


class ListMeta(ABCMeta):
    def __getitem__(self, item):
        return self(item)


class List(AbstractMarker, metaclass=ListMeta):
    def __init__(self, type):
        self.type = type

    def generate(self, countainer, **kwargs):
        raise NotImplementedError()

    def restore(self, countainer, value, **kwargs):
        return [
            restore(self.type(value), countainer, item, **kwargs)
            for item in value
        ]
