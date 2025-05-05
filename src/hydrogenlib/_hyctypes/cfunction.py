import ctypes
from dataclasses import dataclass
from inspect import Signature
from typing import Optional, Union

from .const import CallStandard as CS
from .type_mapping import DefaultMapping
from .._hycore.type_func import Function


class CFunctionflag:
    INPUT = 1
    OUTPUT = 2
    OPTIONAL = 4
    PTR = 8

    def __call__(self, flags, name, default=0):
        return flags, name, default


C_FunctionFlag = CFunctionflag()


@dataclass
class CFunctionPrototype:
    name_or_ordinal: Union[str, int]
    argtypes: Optional[list[type]]
    restype: Optional[type]
    signature: Signature

    call_standard = CS.AUTO
    cdecl_functype = None
    win_functype = None

    @classmethod
    def from_function(cls, func, type_mapping=DefaultMapping):
        func = Function(func)

        argtypes = []

        st = func.signature

        for param in st.parameters.values():
            if param.annotation is not param.empty:
                argtypes.append(type_mapping.map(param.annotation))

        restype = type_mapping.map(
            st.return_annotation if st.return_annotation is not st.empty else None)
        return cls(func.name, argtypes, restype, st)

    def generate_cfunctype(self):
        if self.call_standard == CS.STDCALL:
            self.cdecl_functype = functype = ctypes.CFUNCTYPE(self.restype, *self.argtypes)
        else:
            self.win_functype = functype = ctypes.WINFUNCTYPE(self.restype, *self.argtypes)

        return functype

    def generate_paramflags(self):
        flags = []  # type: list[tuple[int, str, int]]
        for param in self.signature.parameters.values():
            if param.default is param.empty:
                flags.append(C_FunctionFlag(0, param.name))
            else:
                # flags.append(C_FunctionFlag(C_FunctionFlag.OPTIONAL, param.name, param.default))
                flags.append(C_FunctionFlag(1, param.name, param.default))  # 为什么设置为4会报错???
        return tuple(flags)


class CFunction:
    def __init__(self, func, dll=None):
        self._func = Function(func)
        self._callable = None
        self._prototype = CFunctionPrototype.from_function(self._func)

        self._dll = dll

        if self._dll is not None:
            self._dll = dll
            self._prototype.call_standard = dll.call_standard
            self.connect(dll)  # 连接dll

    @classmethod
    def define(cls, dll):
        def wrapper(func):
            return cls(func, dll)

        return wrapper

    @property
    def func(self):
        return self._func

    def connect(self, dll):
        """
        将函数原型与dll连接
        """
        self._callable = dll.register(self._prototype)

    def __call__(self, *args, **kwargs):
        return self._callable(*args, **kwargs)
