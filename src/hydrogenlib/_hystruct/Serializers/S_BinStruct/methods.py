import builtins
import sys
from types import NoneType
from typing import Union

import src.hydrogenlib._hycore.neostruct
from ...._hycore import type_func


def get_class(equal_name: str):
    cls = type_func.get_attr_by_path(equal_name, {'builtins': builtins, **sys.modules})
    return cls


def get_attr_bitmap_length(number_of_attrs: int):
    return (number_of_attrs + 7) // 8


def length_to_bytes(length_or_obj):
    length = length_or_obj if isinstance(length_or_obj, int) else len(length_or_obj)
    return src.hydrogenlib._hycore.neostruct.pack_variable_length_int(length)


def connect_length(bytes_data: Union[bytes, NoneType], no_none=True):
    if not no_none and bytes_data is None:  # NoneType
        return b''
    return b''.join([
        length_to_bytes(bytes_data), bytes_data
    ])


def get_length_offset(offset):
    length, con = src.hydrogenlib._hycore.neostruct.unpack_variable_length_int(offset.surplus(bytes))
    offset += con
    return length


def get_part(offset) -> bytes:
    length = get_length_offset(offset)
    return offset >> length
