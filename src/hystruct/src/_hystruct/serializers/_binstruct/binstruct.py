import typing
from threading import Lock
from typing import Union

from .. import abc
from .struct_abc import BinStructBase
from ...._hycore.type_func import get_qualname

from . import serializer_methods as methods


class Struct(abc.AbstractSerializer):
    struct = BinStructBase

    def dumps(self, data: Union[BinStructBase, typing.Any]):
        if isinstance(data, self.struct):
            return methods.pack(data)
        else:
            return methods.mini_pack(data)

    def loads(self, data, __data__=None, mini=False):
        if mini is True:
            return methods.mini_unpack(data)
        elif mini is False:
            return methods.unpack(data, __data__=__data__)
        else:
            try:
                return methods.unpack(data, __data__=__data__)
            except:
                return methods.mini_unpack(data)


struct_types = {}
_flush_lock = Lock()


def register(cls: Union[BinStructBase, type], name=None):
    name = name or get_qualname(cls)
    if name in struct_types:
        raise ValueError(f"{name} is already registered")
