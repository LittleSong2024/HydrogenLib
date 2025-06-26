# Type hints
import builtins
import ctypes
import types
import typing
from typing import Sequence

import _hycore.type_func

if typing.TYPE_CHECKING:
    from .pointer import Pointer as PointerType, Ref as RefType


class _SelfRef:
    """
    No type hints.
    """


type StructureType = ctypes.Structure | ctypes.Union | ctypes.BigEndianStructure | ctypes.LittleEndianStructure
SelfRef = _SelfRef()  # 自引用

# type int = int
type uint = int
type short = int
type ushort = int
type long = int
type longlong = int
type ulong = int
type ulonglong = int
type double = float
type longdouble = float
type char = int  # uint8_t
type wchar = int  # uint16_t
# type char_p = bytes | None
# type wchar_p = str | None
# char_p 和 wchar_p 不需要另外表示
type void_p = int

type size_t = int
type ssize_t = int
type time_t = int

type int8_t = int
type int16_t = int
type int32_t = int
type int64_t = int
type uint8_t = int
type uint16_t = int
type uint32_t = int
type uint64_t = int

type byte = int
type ubyte = int

type bool = int | builtins.bool | None | object

type Anonymous[T] = T
type Array[T, N] = Sequence[T]
type Pointer[T] = int | None | T  # 正常来说, hyctypes 会执行自动转换为指针类型
type Ref[T] = int | None | T | RefType
type VariableLengthArguments = None  # 占位符

py_to_c_mapping = {
    int: ctypes.c_int,
    float: ctypes.c_float,
    str: ctypes.c_char_p,
    bytes: ctypes.c_char_p,  # char*
    bool: ctypes.c_bool,
    None: ctypes.c_void_p,  # void*
    uint: ctypes.c_uint,
    short: ctypes.c_short,
    ushort: ctypes.c_ushort,
    long: ctypes.c_long,
    longlong: ctypes.c_longlong,
    ulong: ctypes.c_ulong,
    ulonglong: ctypes.c_ulonglong,
    double: ctypes.c_double,
    longdouble: ctypes.c_longdouble,
    char: ctypes.c_byte,  # int8_t
    wchar: ctypes.c_wchar,  # 通常用于宽字符
    void_p: ctypes.c_void_p,
    size_t: ctypes.c_size_t,
    ssize_t: ctypes.c_ssize_t,
    time_t: ctypes.c_long,  # 假设为32位系统上的time_t
    int8_t: ctypes.c_int8,
    int16_t: ctypes.c_int16,
    int32_t: ctypes.c_int32,
    int64_t: ctypes.c_int64,
    uint8_t: ctypes.c_uint8,
    uint16_t: ctypes.c_uint16,
    uint32_t: ctypes.c_uint32,
    uint64_t: ctypes.c_uint64,
    byte: ctypes.c_byte,
    ubyte: ctypes.c_ubyte,
}

c_to_py_mapping = {v: k for k, v in py_to_c_mapping.items()}


def is_alias_type(tp):
    return isinstance(tp, typing.TypeAliasType)


def is_generic_alias_type(tp):
    return isinstance(tp, types.GenericAlias)


def pointer_parse(tp):
    return typing.get_args(tp)[0]


def array_parse(tp):
    return typing.get_args(tp)


def ref_parse(tp):
    return typing.get_args(tp)[0]


def anonymous_parse(tp):
    return typing.get_args(tp)[0]


def as_ctype(tp):
    if is_alias_type(tp):
        return py_to_c_mapping[tp]
    elif is_generic_alias_type(tp):
        origin = typing.get_origin(tp)
        match origin:
            case otp if otp is Pointer:
                ptr_type = pointer_parse(tp)
                return ctypes.POINTER(as_ctype(ptr_type))  # 注意对类型进行二次转换

            case opt if opt is Array:
                array_type, array_len = array_parse(tp)
                return as_ctype(array_type) * array_len  # Ctypes array 的创建方式是乘法

            case opt if opt is Anonymous:
                anonymous_type = anonymous_parse(tp)
                return as_ctype(anonymous_type)

            case opt if opt is Ref:
                target_type = ref_parse(tp)
                return ctypes.POINTER(as_ctype(target_type))

    elif issubclass(tp, _hycore.type_func.builtin_types):
        return py_to_c_mapping[tp]

    return None


if __name__ == '__main__':
    array_type = as_ctype(Array[int, 100])
    print(array_type, type(array_type))
