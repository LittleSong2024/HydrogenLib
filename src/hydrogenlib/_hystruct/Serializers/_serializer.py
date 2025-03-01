# from . import connect_length
from . import Json
from .S_BinStruct.methods import connect_length as _connect_length, get_part
from .abc import Serializer
from ..._hycore.type_func import Offset, get_subclasses_recursion, get_type_name


# 找不到序列化器
class CannotFindSerializer(RuntimeError): ...


# 序列化器冲突
class SerializerConflict(RuntimeError): ...


class UnsetSerializer(RuntimeError): ...


def dumps(obj, serializer: Serializer = None):
    """
    序列化数据
    :param obj: 需要序列化的对象
    :param serializer: 指定一个序列化器，如果为 None，则使用 Json
    """
    if serializer is None:
        serialier = Json()

    return \
            _connect_length(
                serializer.dumps(obj)
            ) + \
            _connect_length(
                serializer.__class__.__name__.encode()
            )


def loads(data: bytes, serializer: Serializer = None, ignore=False, use_my_serializer=False):
    """
    从字节串反序列化数据
    :param data: 字节串
    :param serializer: 指定一个序列化器，如果为 None，则使用 Json
    :param ignore: 当指定的序列化器与序列化数据中标记的序列化器不一样时,忽略标记的序列化器，使用指定的序列化器
    :param use_my_serializer: 强制使用指定的序列化器,优先级大于ignore
    :except CannotFindSerializer: 找不到标记的序列化器
    :except SerializerConflict: 指定的序列化器与标记的序列化器不一样,且ignore为False
    :except UnsetSerializer: 未设置序列化器
    """
    offset = Offset(data)

    data = get_part(offset)
    serializer_name = get_part(offset).decode()

    subclasses = {
        t.__name__: t
        for t in get_subclasses_recursion(Serializer)
    }

    if serializer_name not in subclasses:
        # raise ValueError(f'标记的序列化器为 {serializer_name}, 但它不是 Serializer 的子类')
        raise ValueError(f'Got {serializer_name}, but it is not a subclass of Serializer')

    final_serializer = subclasses[serializer_name]()

    if (serializer is not None and
            get_type_name(final_serializer) != get_type_name(serializer)):
        if not ignore:  # 两个序列化器不匹配,且不忽略错误
            # raise ValueError(f'指定的序列化器与标记的序列化器不匹配')
            raise ValueError(f'Specified serializer does not match the marked serializer')

    if use_my_serializer:  # 当use_my_serializer为True时,使用指定的序列化器
        final_serializer = serializer

    if final_serializer is None:
        raise UnsetSerializer()

    return final_serializer.loads(data)
