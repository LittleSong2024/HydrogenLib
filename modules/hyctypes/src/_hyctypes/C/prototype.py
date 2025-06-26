from _hycore.type_func import get_signature, get_name
from .methods import *


class ProtoType:
    def __init__(self, *argtypes, restype=None, name: str = None):
        self.argtypes = argtypes
        self.restype = restype
        self.name = name

    @classmethod
    def from_pyfunc(cls, maybe_func=None, name: str = None):
        def decorator(func):
            nonlocal name

            name = name or get_name(func)
            signature = get_signature(func)
            types = get_types_from_signature(signature)
            restype = signature.return_annotation

            return cls(*types, restype=restype, name=name)

        if maybe_func is None:
            return decorator
        else:
            return decorator(maybe_func)
