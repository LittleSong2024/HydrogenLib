from types import NoneType
from typing import Literal

from .binary_tree import *
from .bitmap import *
from .dict_func import *
from .function import *
from .index_offset import *
from .list_func import *
from .number import *
from .safe_eval import *
from .tempalte_type import *
from .type_func import *

builtin_types = Union[int, float, str, bool, NoneType, list, tuple, dict, set, bytes, bytearray]


def int_to_bytes(num: int, lenght, byteorder: Literal["little", "big"] = 'little'):
    try:
        byte = num.to_bytes(lenght, byteorder)
    except OverflowError as e:
        raise e
    return byte


def int_to_bytes_nonelength(num: int):
    length = len(hex(num))
    length = max(length // 2 - 1, 1)  # 十六进制下,每两个字符占一个字节
    return num.to_bytes(length, 'little')


def bytes_to_int(data: bytes, byteorder: Literal["little", "big"] = 'little'):
    if len(data) == 0:
        return
    return int.from_bytes(data, byteorder)


def get_vaild_data(data: bytes) -> bytes:
    """
    100100 -> vaild = 1001
    111100 -> vaild = 1111
    :param data:
    :return:
    """
    # 找到第一个有效数据（逆序），他的后面就是无效数据
    after_data = data[::-1]
    for index, value in enumerate(after_data):
        if value != 0:
            last_invaild = len(data) - index
            return data[:last_invaild]
    return b''


def is_error(exception) -> bool:
    return isinstance(exception, Exception)


def get_attr_by_path(path, obj):
    """
    :param path: 引用路径
    :param obj: 起始对象

    """
    path_ls = path.split(".")
    cur = obj
    for attr in path_ls:
        cur = getattr(cur, attr)
    return cur


def set_attr_by_path(path, obj, value):
    path_ls = path.split(".")
    last_index = len(path_ls) - 1
    cur = obj
    for i, attr in enumerate(path_ls):
        if i == last_index:
            setattr(cur, attr, value)
        else:
            cur = getattr(cur, attr)


def get_type_name(origin_data):
    return origin_data.__class__.__name__
