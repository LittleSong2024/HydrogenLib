import ctypes
import platform
from types import FunctionType

from .cfunction import *
from .._hyoverload import overload
from . import quick_define as _qdefine, all_types

STDCALL = 0
CDECL = 1


class HyDll:
    def __init__(self, name, call_type=None):
        if call_type is None:
            if platform.system() == 'Windows':
                call_type = STDCALL
            elif platform.system() in {'Linux', 'Darwin'}:
                call_type = CDECL

        if call_type == STDCALL:
            self.dll = ctypes.windll.LoadLibrary(name)
        elif call_type == CDECL:
            self.dll = ctypes.cdll.LoadLibrary(name)
        else:
            raise ValueError('call_type must be STDCALL or C')

        self.cfunctions = {}
        self.bind_functions = {}

    def _add_bind_function(self, func: CFunction):
        if func.qualname not in self.bind_functions:
            self.bind_functions[func.qualname] = [func]
        else:
            self.bind_functions[func.qualname].append(func)
        return func

    def __define(self, func, name=None):
        func = CFunction(func)
        name = name or func.name
        if name in self.cfunctions:
            func = self.cfunctions[name]

        return self._add_bind_function(func.generate_c_signature(getattr(self.dll, name)))

    @overload
    def define(self, func: FunctionType):
        return self.__define(func)

    @overload
    def define(self, name: str):
        def wrapper(func):
            return self.__define(func, name)

        return wrapper

    def quick_define(self, string, globals=None, locals=None):
        if globals is None:
            globals = vars(all_types)
        func = _qdefine.Function.from_string(string, globals, locals)
        cfunc = CFunction(None, self.dll, func.generate_c_signature(
            getattr(self.dll, func.name)
        ))
        return self._add_bind_function(cfunc)

    def __call__(self, func):
        return self.define(func)

    def __getattr__(self, item):
        if item in self.cfunctions:
            return self.cfunctions[item]
        else:
            return self.dll.__getattr__(item)
