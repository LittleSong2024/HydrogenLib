import ctypes
from dataclasses import dataclass

from . import C


@dataclass
class Dll_Function:
    prototype: C.Prototype
    name_or_ordinal: str
    parent: 'HyDll'

    functype = None
    functype_callable = None
    functype_paramflags = None
    call_standard = CS.AUTO

    def __call__(self, *args, **kwargs):
        if self.functype_callable is None:  # 懒加载
            self.functype = self.prototype.generate_cfunctype()
            self.functype_paramflags = self.prototype.paramflags
            # print(self.functype_paramflags)
            self.functype_callable = self.functype((self.name_or_ordinal, self.parent.dll), self.functype_paramflags)

        return self.functype_callable(*args, **kwargs)


class HyDll:
    def __init__(self, name, conv = CS.AUTO):
        self.conv = conv  # calling convention

        if conv == CS.STDCALL:
            self.dll = ctypes.WinDLL(name)
        elif conv == CS.CDECL:
            self.dll = ctypes.CDLL(name)
        else:
            raise ValueError("Invalid call type")

        self._c_functions = {}

    def __add_function(self, name, prototype):
        func = Dll_Function(prototype, name, self)
        self._c_functions[name] = func
        return func

    def register(self, prototype, name_or_ordinal=None):
        name_or_ordinal = name_or_ordinal or prototype.name_or_ordinal
        return self.__add_function(name_or_ordinal, prototype)

    def __getattr__(self, item):
        if item in self._c_functions:
            return self._c_functions[item]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")
