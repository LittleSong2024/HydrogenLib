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

from .dll import HyDll, CDECL, STDCALL
from .universality import HyStructure


from .methods import *

from . import all_types as types_namespace

from .all_types import *
