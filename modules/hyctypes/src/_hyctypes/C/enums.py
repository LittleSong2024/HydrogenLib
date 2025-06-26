from enum import *


class CallingConvention(IntEnum):
    """
    调用约定
    """

    cdecl = 0
    stdcall = 1
    fastcall = 2
    vectorcall = 3
    pythoncall = 4

    # 目前 ctypes 只支持这些调用约定
