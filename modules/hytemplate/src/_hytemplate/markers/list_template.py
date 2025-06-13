from abc import ABCMeta
from typing import Callable, Any

from ..abstract import AbstractMarker
from ..basic_methods import generate
from ..context import RestorationContext


class ListMeta(ABCMeta):
    def __getitem__(cls, **kwargs):
        return cls(**kwargs)


class ListTemplate(AbstractMarker, metaclass=ListMeta):
    """
    List marker
    :param type: type of list item
    """

    def __init__(self,
                 type: Callable[[Any], Any],
                 source=None,
                 handler: Callable[[Any, int], Any] = (lambda item, index: item)):
        self.type = type
        self.source = source
        self.handler = handler

    def generate(self, context):
        lst = generate(self.source, context.new(parent=self))
        return [self.handler(item, index) for index, item in enumerate(lst)]

    def restore(self, context: RestorationContext):
        return [
            self.type(item)
            for item in context.value
        ]
