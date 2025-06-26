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
from .C.type_hints import *

