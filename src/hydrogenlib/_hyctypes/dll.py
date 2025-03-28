import ctypes

from .methods import *

STDCALL = 0
C = 1


class HyDll:
    def __init__(self, name, call_type=STDCALL):
        if call_type == STDCALL:
            self.dll = ctypes.windll.LoadLibrary(name)
        elif call_type == C:
            self.dll = ctypes.cdll.LoadLibrary(name)
        else:
            raise ValueError('call_type must be STDCALL or C')

        self.cfunctions = {}
        self.bind_functions = {}

    def _add_bind_function(self, func):
        if func.name not in self.bind_functions:
            self.bind_functions[func.name] = [func]
        else:
            self.bind_functions[func.name].append(func)
        return func

    def function(self, func):
        func = CFunction(func)
        if func.name in self.cfunctions:
            func = self.cfunctions[func.name]

        return self._add_bind_function(func.generate_c_signature(getattr(self.dll, func.name)))
