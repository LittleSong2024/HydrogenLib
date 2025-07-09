import ctypes

from .base import AbstractCData
from _hycore.typefunc import as_address_string


class Pointer[T](AbstractCData):
    __ctype__ = ctypes.POINTER

    def __init__(self, obj):
        if isinstance(obj, AbstractCData):
            obj = ctypes.pointer(
                AbstractCData.__cconvert__(obj)
            )
        self.__cdata__ = obj

    @property
    def ptr(self) -> 'ctypes.POINTER(T)':
        return self.__cdata__

    @property
    def value(self) -> T:
        return self.__cdata__.contents

    @value.setter
    def value(self, value):
        self.__cdata__.contents = value

    @property
    def address(self):
        return ctypes.addressof(self)

    def as_address(self):
        return int(self.__cdata__)

    @property
    def type(self):
        return self.__cdata__._type_

    @type.setter
    def type(self, tp):
        self.__cdata__._type_ = tp

    def cast(self, tp):
        return self.__class__(ctypes.cast(self.__cdata__, ctypes.POINTER(as_ctype(tp))))

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

    def __cconvert__(self):
        return self.__cdata__

    def __str__(self):
        return \
            f"""<{self.__class__.__name__} {self.type} at {as_address_string(id(self))}, pointer: {self.as_address}>"""


class Ref(AbstractCData):
    __ctype__ = None

    def __init__(self, obj: AbstractCData, offset=0):
        self.__cdata__ = ctypes.byref(AbstractCData.__cconvert__(obj), offset)

    @classmethod
    def from_buffer(cls, source, offset=0):
        raise NotImplementedError

    @classmethod
    def from_buffer_copy(cls, source, offset=0):
        raise NotImplementedError

    @classmethod
    def from_address(cls, address):
        raise NotImplementedError

    def __cconvert__(self):
        return self.__cdata__
