import ctypes
import platform
from dataclasses import dataclass

from .cfunction import CFunctionPrototype
from .const import CallStandard as CS


@dataclass
class _C_HyDll_Function:
    prototype: CFunctionPrototype
    name_or_ordinal: str
    parent: 'HyDll'

    functype = None
    functype_callable = None
    functype_paramflags = None
    call_standard = CS.AUTO

    def __call__(self, *args, **kwargs):
        if self.functype_callable is None:  # 懒加载
            self.functype = self.prototype.generate_cfunctype()
            self.functype_paramflags = self.prototype.generate_paramflags()
            self.functype_callable = self.functype((self.name_or_ordinal, self.parent.dll), self.functype_paramflags)

        return self.functype_callable(*args, **kwargs)


class HyDll:
    def __init__(self, name, call_standard = CS.AUTO):
        self.call_standard = call_standard
        if call_standard == CS.STDCALL:
            self.dll = ctypes.WinDLL(name)
        elif call_standard == CS.CDECL:
            self.dll = ctypes.CDLL(name)
        else:
            raise ValueError("Invalid call type")

        self._c_functions = {}

    def __add_function(self, name, prototype):
        self._c_functions[name] = _C_HyDll_Function(prototype, name, self)

    def register(self, prototype, name_or_ordinal=None):
        name_or_ordinal = name_or_ordinal or prototype.name_or_ordinal
        self.__add_function(name_or_ordinal, prototype)
