import ctypes
import os
import platform

from .enums import *
from .c_types import Pointer  # 在这里, 我们使用 PointerImpl 暴露类型时应该暴露 PointerType


def get_system_default_calling_conv():
    match os.name:
        case 'nt':
            return CallingConvention.stdcall
        case 'posix':
            return CallingConvention.cdecl
        case _:
            return CallingConvention.cdecl


class DllPointer(Pointer):
    def __call__(self, *args):
        return self.ptr(*args)  # 不允许 Kwargs


class Dll:
    def __init__(self, name: str, calling_convention: CallingConvention = get_system_default_calling_conv(), load=True):
        self._name = name
        self._calling_convention = calling_convention
        self._dll = None

        if load:
            self.load()

    def load(self):
        match self._calling_convention:
            case CallingConvention.stdcall:
                self._dll = ctypes.WinDLL(self._name)
            case CallingConvention.cdecl:
                self._dll = ctypes.CDLL(self._name)
            case CallingConvention.pythoncall:
                self._dll = ctypes.PyDLL(self._name)
            case x if x in {CallingConvention.fastcall, CallingConvention.vectorcall}:
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

        return DllPointer(ptr)

    def attr(self, name: str, type):
        return self.addr(name).cast(type)
