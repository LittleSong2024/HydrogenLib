import builtins
import typing
from collections import deque
from threading import Lock
from types import NoneType
from typing import Sequence, Optional, Union, final

from .methods import get_class, get_attr_bitmap_length, length_to_bytes, connect_length, get_part
from .. import abc
from .... import type_func, neostruct
from ....type_func import get_qualname, get_subclasses


class GeneraterError(Exception):
    ...


class UnpackError(Exception):
    ...


SimpleTypes = typing.Union[int, str, bytes, float]


def pack_attr(attr_value):
    if isinstance(attr_value, SimpleTypes):
        data = neostruct.pack(attr_value)
        type_name = type_func.get_type_name(attr_value)
    elif isinstance(attr_value, BinStructBase):
        type_name = get_qualname(attr_value)
        data = attr_value.pack()
    elif isinstance(attr_value, Sequence):
        type_name = 'list'
        data = _pack_sequence(attr_value)
    elif isinstance(attr_value, dict):
        type_name = 'dict'
        data = _pack_dict(attr_value)
    elif isinstance(attr_value, NoneType):
        type_name = 'NoneType'
        data = None
    else:
        raise NotImplementedError(f'Unsupported type: {type(attr_value)}')

    return connect_length(type_name.encode()) + connect_length(data, no_none=False)


def unpack_attr(offset):
    type_name = get_part(offset).decode()
    if type_name == 'NoneType':
        return None
    packed_data = get_part(offset)
    if type_name in bin_types:
        origin_data = BinStructBase.unpack(packed_data)
    elif hasattr(builtins, type_name):
        type_ = getattr(builtins, type_name)
        if issubclass(type_, SimpleTypes):
            origin_data = neostruct.unpack(type_, packed_data)
        elif issubclass(type_, list):
            origin_data = _unpack_sequence(packed_data)
        elif issubclass(type_, dict):
            origin_data = _unpack_dict(packed_data)
        else:
            raise NotImplementedError(f'Unsupported built-in type: {type_name}')
    else:
        raise NotImplementedError(f'Unsupported type: {type_name}')

    return origin_data


def _pack_sequence(seq):
    sequence_bytes = b''
    for item in seq:
        sequence_bytes += pack_attr(item)

    return sequence_bytes


def _unpack_sequence(data):
    offset = type_func.Offset(data)
    ls = deque()
    while not offset.isend():
        ls.append(unpack_attr(offset))

    return list(ls)


def _pack_dict(dic: dict):
    dict_bytes = b''
    for key, value in dic.items():
        dict_bytes += pack_attr(key)
        dict_bytes += pack_attr(value)
    return dict_bytes


def _unpack_dict(data):
    offset = type_func.IndexOffset.Offset(data)
    result_dict = {}
    while not offset.isend():
        key = unpack_attr(offset)
        value = unpack_attr(offset)
        result_dict[key] = value
    return result_dict


class BinStructBase:
    """

    # 二进制结构体基类

    方法:
        - pack() **不可覆写**, 打包结构体
        - unpack(data) 解包结构体
    属性:
        - _data_ 需要打包的属性**列表**

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
        for name, value in zip(self.__data__, args):
            setattr(self, name, value)
            names.add(name)

        for name, value in kwargs.items():
            if name in names:
                raise ValueError(f'Duplicate name: {name}')
            setattr(self, name, value)

    @final
    def pack(self, *args, **kwargs):
        """
        打包结构体
        :param args: 构造函数参数
        :param kwargs: 构造函数参数
        """

        # | Name | AttrMapping | (Value, Type) pairs |

        pack_event = self.pack_event(*args, **kwargs)
        if pack_event is not True:
            raise GeneraterError('Pack event failed', pack_event)

        __data__ = self.__data__

        this_name = get_qualname(self)
        this_length_head = length_to_bytes(this_name)

        part_name = this_length_head + this_name.encode()

        bitmap = type_func.Bitmap()

        for index, attr in enumerate(__data__):
            origin_data = getattr(self, attr)
            if hasattr(self.__class__, attr):
                if origin_data is getattr(self.__class__, attr):
                    continue  # 未修改的属性, 跳过
            bitmap[index] = True

        part_bitmap = bitmap.pack()

        part_kvpairs = b''

        for i, attr in enumerate(__data__):
            on = bitmap[i]
            if not on:
                continue

            value = self.pack_attr_event(attr)
            current_part = pack_attr(value)
            part_kvpairs += current_part

        packed_data = (
                part_name + part_bitmap + part_kvpairs
        )
        # print(
        #     'Pack:::\n\t',
        #     'Part::Name=', part_name,
        #     '\n\t',
        #     'Part::Bitmap=', part_bitmap, bitmap,
        #     '\n\t',
        #     'Part::KVPairs=', part_kvpairs
        # )

        return packed_data

    @staticmethod
    @final
    def unpack(data, *args, **kwargs):
        """
        解包结构体.
        :param data: 原始数据
        :param args: 传递给unpack_event函数的参数
        :param kwargs: 传递给unpack_event函数的参数
        """

        offset = type_func.IndexOffset.Offset(data)
        this_name = get_part(offset).decode()

        # print(this_name)
        typ = get_class(this_name)

        bitmap_length = get_attr_bitmap_length(len(typ.__data__))
        bitmap = type_func.Bitmap.unpack(offset >> bitmap_length)

        # 获取已设置的属性
        set_attrs = [attr_name for attr_name, on in zip(typ.__data__, bitmap) if on]
        # print(set_attrs)
        temp_dct = {}

        attr_count = 0
        while not offset.isend():
            origin_data = unpack_attr(offset)
            temp_dct[attr_count] = origin_data
            attr_count += 1

        attr_dct = {}

        for attr, value in temp_dct.items():
            attr_dct[set_attrs[attr]] = value

        ins = typ(**attr_dct)  # type: BinStructBase
        Res = ins.unpack_event(*args, **kwargs)
        if Res is not None:
            if type_func.is_errortype(Res):
                raise UnpackError('An error occurred during unpacking') from Res
        return ins

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
            if hasattr(obj, '_data_'):
                __data__ = getattr(obj, '_data_')

        if __data__ is None:
            raise GeneraterError('无法确定结构体需要包含的属性')

        ins = cls(**{name: getattr(obj, name) for name in __data__})
        return ins

    @classmethod
    def is_registered(cls):
        """
        检查此类是否已经注册
        """
        return get_qualname(cls) in bin_types

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


class Struct(abc.Serializer):
    struct = BinStructBase

    def dumps(self, data: BinStructBase):
        return data.pack()

    def loads(self, data):
        return self.struct.unpack(data)


bin_types = {
    get_qualname(BinStructBase),
}

_flush_lock = Lock()


def flush_bin_types():
    """
    为了保证自定义的BinStruct子类能被正确解析,需要调用此函数刷新结构体注册表
    """
    with _flush_lock:
        global bin_types
        bin_types |= set((get_qualname(cls) for cls in get_subclasses(BinStructBase)))


def get_bin_types():
    return bin_types.copy()
