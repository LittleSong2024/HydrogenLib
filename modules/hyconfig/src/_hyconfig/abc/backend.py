import typing
from abc import ABC, abstractmethod
from typing import Self

if typing.TYPE_CHECKING:
    from .model import AbstractModel


class AbstractBackend(ABC):
    __support_types__ = None

    def __support_compare(self, type):
        return type in self.__support_types__

    def __support_check(self, type):
        for i in self.__support_types__:
            if issubclass(type, i):
                return True
        return False

    def __init_subclass__(cls, **kwargs):
        if cls.__support_types__ is None:
            raise TypeError("BackendABC subclass must have a support_types attribute.")

    def __class_getitem__(cls, item) -> 'AbstractBackend':
        return cls().set_model(item)

    def support(self, type):
        return self.__support_compare(type) or self.__support_check(type)

    @abstractmethod
    def set_model(self, model: 'AbstractModel') -> Self:
        ...

    @abstractmethod
    def get_model(self) -> 'AbstractModel':
        ...

    @abstractmethod
    def save(self, fd):
        ...

    @abstractmethod
    def load(self, fd):
        ...
