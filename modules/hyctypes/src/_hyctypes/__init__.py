"""
Use:
    import ...
    dll = Dll('user32')

    @ProtoType.from_pyfunc
    def MessageBoxW(hwnd: int, text: str, caption: str, uType: int) -> int: ...

    dll.connect(MessageBoxW)

"""


from . import C
from .C.enums import CallingConvention as CallingConv
from .C.function import Function, Method, WrapedArguments
from .C.prototype import ProtoType
from .C.dll import Dll, DllPointer


from .C.c_types import *

from .C.compound_types import (
    PointerType as Pointer,
    RefType as Ref,
    ArrayType as Array,
    StructureType as Structure,
    Structure as StructureBase,
    UnionType as Union
)



