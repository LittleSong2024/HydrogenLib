from typing import *
from inspect import Signature
from .const import CallingConvention as CS


@dataclass
class Prototype:
    name_or_ordinal: Union[str, int]
    argtypes: Optional[list[type]]
    restype: Optional[type]
    signature: Signature

    call_standard = CS.AUTO
    cdecl_functype = None
    win_functype = None

    @classmethod
    def from_function(cls, func, type_mapping=DefaultMapping):
        func = Function(func)

        argtypes = []

        st = func.signature

        for param in st.parameters.values():
            if param.annotation is not param.empty:
                argtypes.append(type_mapping.map(param.annotation))

        restype = type_mapping.map(
            st.return_annotation if st.return_annotation is not st.empty else None)
        return cls(func.name, argtypes, restype, st)

    def generate_cfunctype(self):
        if self.call_standard == CS.STDCALL:
            self.cdecl_functype = functype = ctypes.CFUNCTYPE(self.restype, *self.argtypes)
        else:
            self.win_functype = functype = ctypes.WINFUNCTYPE(self.restype, *self.argtypes)

        return functype

    @property
    def paramflags(self):
        flags = []  # type: list[tuple[int, str, int]]
        for param in self.signature.parameters.values():
            if param.default is param.empty:
                flags.append(C.ParamFlags(0, param.name))
            else:
                # flags.append(C_FunctionFlag(C_FunctionFlag.OPTIONAL, param.name, param.default))
                flags.append(C.ParamFlags(1, param.name, param.default))  # 为什么设置为4会报错???
        return tuple(flags)