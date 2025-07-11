from _hycore.typefunc import alias
from .base import *
from ..basic_types.type_realities import ubyte


class Pointer(AbstractCData):
    __slots__ = ()

    ptr = alias['__cdata__'](mode=alias.mode.read_write)

    def __init__(self, ptr):
        self.ptr = ptr

    def cast(self, tp):
        return cast(self, tp)

    @property
    def value(self):
        return self.ptr.contents

    @value.setter
    def value(self, v):
        c_obj = as_cdata(v)
        c_type = type(c_obj)
        if not issubclass(c_type, self.ptr._type_):
            raise TypeError(f'{c_type} cannot be assigned to {self.ptr._type_}')  # 无法使指针指向另一类型的对象

        self.ptr.contents = c_obj

    @classmethod
    def from_integer(cls, address: int, type=None):
        ptr = cls(None)
        ptr.ptr = ctypes.POINTER(type)(address)
        return ptr

    def __getitem__(self, item):
        return self.ptr[item]

    def __convert_ctype__(self, target):
        from .type_realities import PointerType, RefType
        if not isinstance(target, (PointerType, RefType)):
            raise TypeError(f'{Pointer} cannot be assigned to {target}')

        return cast(self, as_ctype(target))


class Ref(AbstractCData):
    __slots__ = ()

    ref = alias['__cdata__'](mode=alias.mode.read_write)

    def __init__(self, obj):
        self.ref = byref(obj)

    def __convert_ctype__(self, target):
        raise NotImplementedError


class Array(AbstractCData):
    array = alias['__cdata__'](mode=alias.mode.read_write)

    def __init__(self, array):
        self.array = array

    @property
    def length(self):
        return self.array._length_

    @property
    def element_type(self):
        return self.array._type_

    @property
    def np_array(self):
        import numpy as np
        return np.ctypeslib.as_array(self.array)

    def __len__(self):
        return self.length

    def __getitem__(self, item):
        return self.array[item]

    def __setitem__(self, item, value):
        self.array[item] = value


class ArrayPointer(Array):

    length = alias['_length']

    @property
    def element_type(self):
        return self._type

    @element_type.setter
    def element_type(self, type):
        self._type = type
        self.array = cast(self.array, type)  # 将指针的元素类型改为type

    def __init__(self, pointer, length=1, type=ubyte):
        super().__init__(pointer)
        self._length = length
        self._type = type

    def check(self, index):
        if index < 0:
            index += self.length

        if index >= self.length or index < 0:
            raise IndexError(f"Index {index} out of range.")

        return index

    def __getitem__(self, index):
        return super().__getitem__(self.check(index))

    def __setitem__(self, index, value):
        super().__setitem__(self.check(index), value)


class Structure(AbstractCData):
    def __init__(self, struct):
        self.__cdata__ = struct
        self.__ctype__ = struct.__class__

    def __getattr__(self, name):
        return getattr(self.__cdata__, name)

    def __setattr__(self, name, value):
        if hasattr(self, name):
            super().__setattr__(name, value)
        else:
            setattr(self.__cdata__, name, value)

    def __convert_ctype__(self, target):
        from .type_realities import PointerType, RefType

        if isinstance(target, PointerType):
            return Pointer(pointer(self))
        elif isinstance(target, RefType):
            return Ref(self)
        else:
            raise NotImplementedError

    def __str__(self):
        head = f"struct {self.__class__.__name__}:\n"
        body = ''
        for field, type in self.__ctype__._fields_:
            value = getattr(self, field)
            body += f"\t{field} = {value}  # type: {type.__name__}\n"

        return head + body

    def __repr__(self):
        field_dct = {
            k: getattr(self, k) for k in self.__ctype__._fields_
        }
        return f"{self.__class__.__name__}({', '.join([f'{field}={value}' for field, value in field_dct.items()])})"


