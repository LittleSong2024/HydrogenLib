import ctypes

from .pointer_type import Pointer as _Pointer, Ref as _Ref
from .array_type import Array as _Array


class CType:
    __real_type__: type

    def __init_subclass__(cls, **kwargs):
        real = kwargs.get('real')
        if real:
            cls.__real_type__ = real

    def __class_getitem__(cls, *item):
        return cls(*item)

    def __call__(self, *args, **kwargs) -> '__real_type__':
        return self.__real_type__(*args, **kwargs)


class Pointer(CType, real=_Pointer):
    def __init__(self, target_type):
        self._target_tp = target_type


class Ref(CType, real=_Ref):
    def __init__(self, target_type):
        self._target_tp = target_type


class Array(CType, real=_Array):
    def __init__(self, target_type, length):
        self._target_tp = target_type
        self._length = length

    def __call__(self, *args):
        array = _Array(self._target_tp, self._length, *args)
        return array


uint = ctypes.c_uint
short = ctypes.c_short
ushort = ctypes.c_ushort
long = ctypes.c_long
longlong = ctypes.c_longlong
ulong = ctypes.c_ulong
ulonglong = ctypes.c_ulonglong
double = ctypes.c_double
longdouble = ctypes.c_longdouble

void_p = ctypes.c_void_p

size_t = ctypes.c_size_t
ssize_t = ctypes.c_ssize_t
time_t = ctypes.c_time_t

int8_t = ctypes.c_int8
int16_t = ctypes.c_int16
int32_t = ctypes.c_int32
int64_t = ctypes.c_int64
uint8_t = ctypes.c_uint8
uint16_t = ctypes.c_uint16
uint32_t = ctypes.c_uint32
uint64_t = ctypes.c_uint64

byte = ctypes.c_byte
ubyte = ctypes.c_ubyte

bool = ctypes.c_bool

