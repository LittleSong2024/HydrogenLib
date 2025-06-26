import ctypes
import os
import platform

from .enums import *

from .dll_pointer import DLLPointer


def get_system_default_calling_conv():
    match os.name:
        case 'nt':
            return CallingConvention.stdcall
        case 'posix':
            return CallingConvention.cdecl
        case _:
            return CallingConvention.cdecl


class Dll:
    def __init__(self, name: str, calling_convention: CallingConvention = get_system_default_calling_conv(), load=True):
        self._name = name
        self._calling_convention = calling_convention
        self._cdll = None

        if load:
            self.load()

    def load(self):
        match self._calling_convention:
            case CallingConvention.stdcall:
                self._cdll = ctypes.WinDLL(self._name)
            case CallingConvention.cdecl:
                self._cdll = ctypes.CDLL(self._name)
            case CallingConvention.pythoncall:
                self._cdll = ctypes.PyDLL(self._name)
            case CallingConvention.fastcall, CallingConvention.vectorcall:
                match platform.system():
                    case "Windows":
                        self._cdll = ctypes.WinDLL(self._name)
                    case "Linux", "Darwin":
                        self._cdll = ctypes.CDLL(self._name)
                    case _:
                        raise Exception("Unsupported OS")

    @property
    def name(self):
        return self._name

    @property
    def calling_convention(self):
        return self._calling_convention

    @property
    def cdll(self):
        return self._cdll

    def ready(self):
        return self._cdll is not None

    def addr(self, name_or_index: str | int) -> DLLPointer:
        return DLLPointer(self._cdll, name_or_index)

    def attr(self, name: str, type):
        return self.addr(name).cast_value(type)

