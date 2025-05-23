import typing
from abc import ABC, abstractmethod
from typing import Protocol, Self, Union, runtime_checkable, Optional, Any

from _hycore.type_func import get_qualname
from _hystruct.serializers._binstruct.binstruct import struct_types
from _hystruct.serializers._binstruct.errors import GeneraterError


@runtime_checkable
class Packable_CLS_NO_ARG(Protocol):
    def pack(self, ins) -> bytes:
        ...


@runtime_checkable
class Packable_INS_NO_ARG(Protocol):
    def pack(self) -> bytes:
        ...


@runtime_checkable
class Packable_CLS_WITH_ARG(Protocol):
    @classmethod
    def pack(cls, ins, *args, **kwargs) -> bytes:
        ...


@runtime_checkable
class Packable_INS_WITH_ARG(Protocol):
    def pack(self, *args, **kwargs) -> bytes:
        ...


@runtime_checkable
class Unpackable_CLS_NO_ARG(Protocol):
    @classmethod
    def unpack(cls, data: bytes) -> 'Self':
        ...


@runtime_checkable
class Unpackable_CLS_WITH_ARG(Protocol):
    @classmethod
    def unpack(cls, data: bytes, *args, **kwargs) -> 'Self':
        ...


@runtime_checkable
class Unpackable_INS_NO_ARG(Protocol):
    def unpack(self, data: bytes) -> 'Self':
        ...


@runtime_checkable
class Unpackable_INS_WITH_ARG(Protocol):
    def unpack(self, data: bytes, *args, **kwargs) -> 'Self':
        ...


PackableNoArg = Union[Packable_CLS_NO_ARG, Packable_INS_NO_ARG]
PackableWithArg = Union[Packable_CLS_WITH_ARG, Packable_INS_WITH_ARG]
Packable = Union[PackableNoArg, PackableWithArg]

UnpackableNoArg = Union[Unpackable_CLS_NO_ARG, Unpackable_INS_NO_ARG]
UnpackableWithArg = Union[Unpackable_CLS_WITH_ARG, Unpackable_INS_WITH_ARG]
Unpackable = Union[UnpackableNoArg, UnpackableWithArg]
SimpleTypes = typing.Union[int, str, bytes, float]


class BinStructBase:
    """

    # 二进制结构体基类
    属性:
        - __data__ 需要打包的属性**列表**

    """
    __data__ = []  # Variables' names

    def pack_event(self, *args, **kwargs):
        """
        打包事件,进行打包前的处理
        """
        return True

    def pack_attr_event(self, attr_name: str):
        return getattr(self, attr_name)

    def unpack_event(self, *args, **kwargs) -> Optional[Union[Exception, bool]]:
        """
        解包事件,解包后对原始数据的重新处理
        """
        return True

    def __init__(self, *args, **kwargs):
        names = set()
        for index, (name, value) in enumerate(zip(self.__data__, args)):
            setattr(self, name, value)
            names.add(name)

        if len(args) > len(self.__data__):
            raise ValueError(f'Too many arguments: {len(args)} > {len(self.__data__)}')

        for name, value in kwargs.items():
            if name in names:
                raise ValueError(f'Duplicate name: {name}')
            setattr(self, name, value)

    @classmethod
    def to_struct(cls, obj, __data__=None):
        """
        根据传入的对象以及__data__列表,构建结构体
        """
        if isinstance(obj, BinStructBase):
            if __data__ is None:
                return obj
            elif __data__ == obj.__data__:
                return obj
            else:
                raise GeneraterError('无法确定结构体需要包含的属性')
        if __data__ is None:
            if hasattr(obj, '__data__'):
                __data__ = getattr(obj, '__data__')

        if __data__ is None:
            raise GeneraterError('无法确定结构体需要包含的属性')

        ins = cls(**{name: getattr(obj, name) for name in __data__})
        ins.__data__ = __data__
        return ins

    @classmethod
    def is_registered(cls):
        """
        检查此类是否已经注册
        """
        return get_qualname(cls) in struct_types

    @property
    def __attrs_dict(self):
        dct = {}
        for name in self.__data__:
            dct[name] = getattr(self, name)
        return dct

    def __str__(self):
        kv_pairs = list(self.__attrs_dict.items())
        return f'{self.__class__.__name__}({", ".join((f"{name}={repr(value)}" for name, value in kv_pairs))})'

    def __eq__(self, other):
        if not isinstance(other, BinStructBase):
            return False
        return self.__attrs_dict == other.__attrs_dict

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple(self.__attrs_dict.items()))

    __repr__ = __str__


class Handler(ABC):
    @abstractmethod
    def packable(self, data) -> bool: ...

    @abstractmethod
    def unpackable(self, data) -> bool: ...

    @abstractmethod
    def pack(self, serializer, data) -> bytes: ...

    @abstractmethod
    def unpack(self, serializer, data) -> Any: ...


class Serializer:
    def __init__(self):
        self.serializer_handlers = []

    def add_handler(self, handler: Handler):
        self.serializer_handlers.append(handler)

    def remove_handler(self, handler: Handler):
        self.serializer_handlers.remove(handler)

    def get_matched_handler(self, data):
        for handler in self.serializer_handlers:
            if handler.packable(data):
                return handler
        return None

    def pack(self, data):
        handler = self.get_matched_handler(data)
        if handler:
            return handler.pack(self, data)
        return None

    def unpack(self, data):
        handler = self.get_matched_handler(data)
        if handler:
            return handler.unpack(self, data)
        return None
