import ctypes

from .const import CallingConvention as CC


# def CFUNCTYPE(restype: Type[_CData] | None,
#               *argtypes: Type[_CData],
#               use_errno: bool = ...,
#               use_last_error: bool = ...) -> Type[_FuncPointer]

class UniverseFunctype:
    def __init__(self, restype, *argtypes, use_errno=False, use_last_error=False, conv=CC.AUTO):
        self.restype = restype
        self.argtypes = argtypes
        self.use_errno = use_errno
        self.use_last_error = use_last_error
        self.conv = conv

        self._functype = None

    @property
    def functype(self):
        if self._functype is None:
            if self.conv == CC.CDECL:
                typ = ctypes.CFUNCTYPE
            elif self.conv == CC.STDCALL:
                typ = ctypes.WINFUNCTYPE
            else:
                raise NotImplementedError()

            self._functype = typ(self.restype, *self.argtypes, use_errno=self.use_errno,
                                 use_last_error=self.use_last_error)

        return self._functype

    def __call__(self, *args, **kwargs):
        return self.functype(*args, **kwargs)
