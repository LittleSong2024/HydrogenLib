from collections import deque
from typing import Sequence

from .errors import GeneraterError
from .methods import *
from .struct_abc import SimpleTypes, BinStructBase
from ...._hycore import neostruct
from ...._hycore.type_func import get_type_name, get_qualname


def pack_attr(attr_value):
    if isinstance(attr_value, SimpleTypes):
        data = neostruct.neopack(attr_value)
        type_name = get_type_name(attr_value)
    elif isinstance(attr_value, BinStructBase):
        type_name = get_qualname(attr_value)
        data = pack(attr_value)
    elif isinstance(attr_value, Sequence):
        type_name = get_type_name(attr_value)
        if type_name not in ['list', 'tuple', 'set']:
            raise NotImplementedError(f'Unsupported type: {type(type_name)}')
        data = _pack_sequence(attr_value)
    elif isinstance(attr_value, dict):
        type_name = 'dict'
        data = _pack_dict(attr_value)
    elif isinstance(attr_value, NoneType):
        type_name = 'NoneType'
        data = None
    else:
        raise NotImplementedError(f'Unsupported type: {type(attr_value)}')

    return add_length(type_name.encode()) + add_length(data, no_none=False)


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
            origin_data = neostruct.neounpack(type_, packed_data)
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
    offset = type_func.Offset(data)
    result_dict = {}
    while not offset.isend():
        key = unpack_attr(offset)
        value = unpack_attr(offset)
        result_dict[key] = value
    return result_dict


def pack(struct, *args, **kwargs):
    """
    打包结构体
    :param args: 构造函数参数
    :param kwargs: 构造函数参数
    """

    # | Name | AttrMapping | (Value, Type) pairs |

    pack_event = struct.pack_event(*args, **kwargs)
    if pack_event is not True:
        raise GeneraterError('Pack event failed', pack_event)

    __data__ = struct.__data__

    pack_attr, unpack_attr = struct.serializer_funcs.get('pack'), struct.serializer_funcs.get('unpack')
    if not (pack_attr and unpack_attr):
        raise NotImplementedError('Pack attr or unpack attr is not defined')

    this_name = get_qualname(struct)
    this_length_head = length_to_bytes(this_name)

    part_name = this_length_head + this_name.encode()

    bitmap = type_func.Bitmap()

    for index, attr in enumerate(__data__):
        origin_data = getattr(struct, attr)
        if hasattr(struct.__class__, attr):
            if origin_data is getattr(struct.__class__, attr):
                continue  # 未修改的属性, 跳过
        bitmap[index] = True

    part_bitmap = bitmap.pack()

    part_kvpairs = b''

    for i, attr in enumerate(__data__):
        on = bitmap[i]
        if not on:
            continue

        value = struct.pack_attr_event(attr)
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


# @final
def unpack(data, __data__=None, *args, **kwargs):
    """
    解包结构体.
    :param data: 原始数据
    :param __data__: 构造函数参数
    :param args: 传递给unpack_event函数的参数
    :param kwargs: 传递给unpack_event函数的参数
    """

    offset = type_func.Offset(data)
    this_name = get_part(offset).decode()

    # print(this_name)
    typ = get_class(this_name)
    # print(typ)

    __data__ = __data__ or typ.__data__

    bitmap_length = get_attr_bitmap_length(len(__data__))
    bitmap = type_func.Bitmap.unpack(offset >> bitmap_length)

    # 获取已设置的属性
    set_attrs = [attr_name for attr_name, on in zip(__data__, bitmap) if on]
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
        if type_func.is_error(Res):
            raise UnpackError('An error occurred during unpacking') from Res
    return ins


def mini_pack(data):
    return serializer_funcs['pack'](data)


def mini_unpack(self, data):
    offset = type_func.Offset(data)
    return self.serializer_funcs['unpack'](offset)  # Unpack 的参数是一个索引偏移对象
