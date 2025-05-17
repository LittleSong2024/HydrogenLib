"""
Use:
    from ctypes import c_int
    dll = HyDll(<dll_name>, <STDCALL | CDECL | None>)

    @dll.define
    def AnyFunction(a: c_int, b: c_int) -> None: ...

    @dll.define
    def ... ( ... ) -> ... : ...
"""

from ctypes import *
from ctypes import util

from .dll import HyDll
from .structure import HyStructure
from .const import CallStandard
from .methods import *
from .cfunction import *

from . import c_types as types_namespace

from .c_types import *
