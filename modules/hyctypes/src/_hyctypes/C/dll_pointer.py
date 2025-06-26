import ctypes


class DLLPointer:
    @property
    def _c_ptr(self):
        try:
            if isinstance(self._identifier, str):
                self.__c_ptr = getattr(self._cdll, self._identifier)
            else:
                self.__c_ptr = self._cdll[self._identifier]
        except AttributeError:
            raise RuntimeError(f"Cannot find function or variable `{self._identifier}` in DLL {self._cdll}") from None

        return self.__c_ptr

    def __init__(self, dll, name_or_index: str, type=None):
        self._cdll = dll
        self._identifier = name_or_index
        self.__c_ptr = None
        self._type = type

    @property
    def value(self):
        return ctypes.cast(self._c_ptr, ctypes.POINTER(self._type)).contents

    def cast_value(self, tp):
        return ctypes.cast(self._c_ptr, ctypes.POINTER(self._type)).contents

    def __call__(self, *args, **kwargs):
        return self._c_ptr(*args, **kwargs)
