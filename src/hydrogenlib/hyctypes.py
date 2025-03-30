import ctypes as _ctypes, os as _os
from ._hyctypes import HyDll, HyStructure
from ctypes import *

if _os.name == 'nt':
    from ctypes.wintypes import *


def POINTER(type):
    if issubclass(type, HyStructure):
        return _ctypes.POINTER(type.c_struct)
    else:
        return _ctypes.POINTER(type)
