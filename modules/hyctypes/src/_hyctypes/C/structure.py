import ctypes
from typing import Any

from _hycore.type_func import get_name
from .base import *
from .type_hints import *
from .pointer import Pointer as Ptr


class Field:
    name = None

    def __init__(self, name):
        self.name = name

    def __get__(self, inst, cls):
        return getattr(inst.__data__, self.name)

    def __set__(self, inst, value):
        setattr(inst.__data__, self.name, value)

    def __delete__(self, inst):
        delattr(inst.__data__, self.name)


class _Structure:
    __data__: Any = None  # ctypes 没有公开所有c类型的基类`CData`, 所以只能将类型设为 Any
    __ctype__: type  # 这个属性放置了定义完成的结构体

    __anonymous__: list[str] = None  # You should set this attribute before setting the fields.
    __fields__: list[str] = None

    __pack__: int = None  # You should set this attribute before setting the fields.
    __align__: int = None  # Add in 3.13

    __structure_type__: type[StructureType]  # 这个属性指定了结构体的类型

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        if kwargs.get('nonstruct', None) is True:
            return
        struct_type = type(get_name(cls), (cls.__structure_type__,), {})
        if cls.__pack__:
            struct_type._pack_ = cls.__pack__ or kwargs.get('pack')
        if cls.__align__:
            struct_type._align_ = cls.__align__ or kwargs.get('align')
        if cls.__anonymous__:
            struct_type._anonymous_ = cls.__anonymous__ or kwargs.get('anonymous')

        struct_type._fields_ = tuple(cls.__fields__)

        cls.__ctype__ = struct_type


class Structure(AbstractCData, _Structure, nonstruct=True):
    __structure_type__ = ctypes.Structure

    def convert(self):
        return self.__data__

    @classmethod
    def from_address(cls, address):
        cls.from_c_inst(cls.__ctype__.from_address(address))

    @classmethod
    def from_buffer_copy(cls, source, offset=0):
        cls.from_c_inst(cls.__ctype__.from_buffer_copy(source, offset))

    @classmethod
    def from_buffer(cls, source, offset=0):
        cls.from_c_inst(cls.__ctype__.from_buffer(source, offset))

    @classmethod
    def from_c_inst(cls, inst):
        s = cls()
        s.__data__ = inst
        return s

    def __init_subclass__(cls, **kwargs):
        fields = []
        for name, anno in cls.__annotations__.items():
            fields.append((name, as_ctype(anno)))
            setattr(cls, name, Field(name))
        cls.__fields__ = fields
        super().__init_subclass__(**kwargs)

    def __init__(self, *args, **kwargs):
        self.__data__ = self.__ctype__(*args, **kwargs)

    def __getitem__(self, item):
        return getattr(self.__data__, item)

    def __setitem__(self, item, value):
        setattr(self.__data__, item, value)

    def __delitem__(self, item):
        delattr(self.__data__, item)

    # ~ 操作符
    def __invert__(self):
        return Ptr(self)

    def __str__(self):
        head = f"struct {self.__class__.__name__}:\n"
        body = ''
        for field, type in self.__fields__:
            value = getattr(self, field)
            body += f"\t{field} = {value}  # type: {type.__name__}\n"

        return head + body

    def __repr__(self):
        field_dct = {
            k: getattr(self, k) for k in self.__fields__
        }
        return f"{self.__class__.__name__}({', '.join([f'{field}={value}' for field, value in field_dct.items()])})"
