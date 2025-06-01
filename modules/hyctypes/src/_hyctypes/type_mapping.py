import typing

from . import c_types as ctypes
from _hycore.utils import InstanceDict


class TypeMapping(InstanceDict):
    def map(self, typ):
        origin = typing.get_origin(typ)
        if origin == typing.Union:
            raise TypeError("Union type not supported")
        if origin == typing.Optional:
            origin = typing.get_args(typ)[0]
        return self.get(origin, default=typ)  # 可以转换的直接转换, 否则返回原值

    def map_sequence(self, seq):
        return [self.map(i) for i in seq]

    @classmethod
    def build(cls, type_mapping: dict):
        return cls(type_mapping)


DefaultMapping = TypeMapping(
    {
        int: ctypes.c_int,
        float: ctypes.c_float,
        str: ctypes.c_wchar_p,
        bool: ctypes.c_bool,
        bytes: ctypes.c_char_p,
        bytearray: ctypes.c_char_p,
    }
)




