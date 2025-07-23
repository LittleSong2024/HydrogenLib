import ctypes
import os
import platform

from .basic_types import CallingConvention as CV
from .c_types import Function, ProtoType


class Dll:
    def __init__(self, name: str, calling_convention: CV = CV.auto, load=True):
        self._name = name
        self._calling_convention = calling_convention
        self._dll = None

        if load:
            self.load()

    def load(self):
        match self._calling_convention:
            case CV.stdcall:
                self._dll = ctypes.WinDLL(self._name)
            case CV.cdecl:
                self._dll = ctypes.CDLL(self._name)
            case CV.pythoncall:
                self._dll = ctypes.PyDLL(self._name)
            case x if x in {CV.fastcall, CV.vectorcall}:
                match platform.system():
                    case "Windows":
                        self._dll = ctypes.WinDLL(self._name)
                    case "Linux", "Darwin":
                        self._dll = ctypes.CDLL(self._name)
                    case _:
                        raise Exception("Unsupported OS")

    @property
    def name(self):
        return self._name

    @property
    def calling_convention(self):
        return self._calling_convention

    @property
    def dll(self):
        return self._dll

    def ready(self):
        return self._dll is not None

    def addr(self, name_or_index: str | int):
        if isinstance(name_or_index, str):
            ptr = getattr(self._dll, name_or_index)
        elif isinstance(name_or_index, int):
            ptr = self._dll[name_or_index]
        else:
            raise TypeError("Unsupported type")

        return ptr

    def attr(self, name: str, type):
        return self.addr(name).cast(type)

    def __getattr__(self, name):
        return self.addr(name)

    def __call__(self, maybe_func=None, *, name: str = None):
        def decorator(func):
            prototype = ProtoType.define(name=name)(func)
            func = Function(self.addr(prototype.name), prototype, prototype.signature)
            return func

        return decorator(maybe_func) if maybe_func else decorator
