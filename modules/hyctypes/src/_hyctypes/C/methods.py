import ctypes
import typing
from types import NoneType

from . import type_hints as th
from .pointer import Pointer, Ref
from .array import ArrayType
from .base import AbstractCData


def get_types_from_signature(signature):
    for param in signature.parameters.values():
        yield param.annotation


def cconvert(value, tp, error=False, default=None):
    if hasattr(value, '__cconvert__'):
        return value.__cconvert__(tp)
    else:
        if error:
            raise TypeError(f'无法转换对象 {value} 为 CData')
        else:
            return default


def type_convert(value, tp):
    origin = typing.get_origin(tp)
    if origin is None:  # 没有设置泛型
        origin = tp

    match origin:
        case x if x in {th.Pointer, th.Ref}:  # 目标是一个指针/引用
            if not isinstance(value, (ctypes.c_void_p, NoneType)):  # 如果不是指针直接可以接收的类型
                if isinstance(value, (Pointer, Ref)):
                    return value.convert()  # Pointer 和  Ref 可以直接转换为指针类型
                elif isinstance(value, int):
                    return ctypes.c_void_p(value)
                elif isinstance(value, AbstractCData):
                    return Pointer.from_object(value)  # AbstractCData 可以转换为指针类型
                else:
                    return type_convert(cconvert(value, origin, error=True), tp)
            else:
                return value  # 它的类型就是指针类型

        case th.Array:
            if not isinstance(value, (ctypes.c_void_p, ctypes.Array)):
                return type_convert(value, th.Pointer)  # 尝试将 value 转换为指针类型
            else:
                return value

        # 剩下的 Anonymous 泛型不需要处理







