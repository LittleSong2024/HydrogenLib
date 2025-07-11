from .basic_types import *
from .compound_types import *
from .py_types import *

AnyPtr = PointerType[None]  # like ctypes.c_void_p
AnyRef = RefType[object]  # ctypes 的 Ref 没有类型, 按照我们的类型框架, 应该用 object
