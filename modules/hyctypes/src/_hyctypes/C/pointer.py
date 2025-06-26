import ctypes

from .base import AbstractCData
from .type_hints import as_ctype


class Pointer[T](AbstractCData):
    __ctype__ = ctypes.POINTER

    def __init__(self, c_ptr):
        self._c_ptr = c_ptr

    @classmethod
    def from_object(cls, obj):
        if isinstance(obj, AbstractCData):
            obj = obj.convert()
        return cls(ctypes.pointer(obj))

    @property
    def c_ptr(self) -> 'ctypes.POINTER(T)':
        return self._c_ptr

    @property
    def value(self) -> T:
        return self._c_ptr.contents

    @value.setter
    def value(self, value):
        self._c_ptr.contents = value

    @property
    def address(self):
        return ctypes.addressof(self.value)

    @property
    def type(self):
        return self._c_ptr._type_

    def cast(self, tp):
        return self.__class__(ctypes.cast(self._c_ptr, ctypes.POINTER(as_ctype(tp))))

    @classmethod
    def from_buffer(cls, source, offset=0):
        c_ptr = cls.__ctype__(None).from_buffer(source, offset)
        return cls(c_ptr)  # 这时候 c_ptr 是一个类型为空的指针

    @classmethod
    def from_buffer_copy(cls, source, offset=0):
        c_ptr = cls.__ctype__(None).from_buffer_copy(source, offset)
        return cls(c_ptr)

    @classmethod
    def from_address(cls, address):
        c_ptr = cls.__ctype__(None).from_address(address)
        return cls(c_ptr)

    def convert(self):
        return self.c_ptr


class Ref(AbstractCData):
    __ctype__ = None

    def __init__(self, obj: AbstractCData, offset=0):
        self._ref = ctypes.byref(obj.convert(), offset)

    @classmethod
    def from_buffer(cls, source, offset=0):
        raise NotImplementedError

    @classmethod
    def from_buffer_copy(cls, source, offset=0):
        raise NotImplementedError

    @classmethod
    def from_address(cls, address):
        raise NotImplementedError

    def convert(self):
        return self._ref
