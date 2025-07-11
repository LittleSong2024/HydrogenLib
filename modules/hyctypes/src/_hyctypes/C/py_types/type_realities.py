import builtins as bt

from .base import AbstractCType


class pytype(AbstractCType):
    def __init__(self, pytype):
        self.pytp = pytype

    def __convert_ctype__(self, obj):
        origin = obj.__class__
        match self.pytp:
            case bt.str:
                match origin:
                    case bt.str: return obj
                    case bt.bytes: return obj.decode()
                    case bt.memoryview: return obj.to_bytes().decode()
                    case _: raise TypeError(f'{origin} cannot convert to {self.pytp}')
            case bt.bytes:
                match origin:
                    case bt.bytes:return obj
                    case bt.str: return obj.encode()
                    case bt.memoryview: return obj.to_bytes()
                    case _: raise TypeError(f'{origin} cannot convert to {self.pytp}')

            case bt.memoryview:
                match origin:
                    case bt.memoryview: return obj
                    case bt.bytes: return memoryview(obj)
                    case bt.str: return memoryview(obj.encode())
                    case _: raise TypeError(f'{origin} cannot convert to {self.pytp}')

            case x:
                return x(obj)

int = pytype[int]
float = pytype[float]
str = pytype[str]
bytes = pytype[bytes]
memoryview = pytype[memoryview]
bytearray = pytype[bytearray]
list = pytype[list]
tuple = pytype[tuple]
dict = pytype[dict]
set = pytype[set]
