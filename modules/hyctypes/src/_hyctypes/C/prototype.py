from _hycore.typefunc import get_signature, get_name
from .methods import *


class ProtoType:
    def __init__(self, *argtypes, restype=None, name: str = None, signature=None):
        self.argtypes = argtypes
        self.restype = restype
        self.name = name

        self.py_signature = signature

    @classmethod
    def from_pysignature(cls, signature, name= None):
        types = get_types_from_signature(signature)
        return cls(*types, name=name, signature=signature)

    @classmethod
    def from_pyfunc(cls, maybe_func=None, name: str = None):
        def decorator(func):
            nonlocal name

            name = name or get_name(func)
            signature = get_signature(func)  # 获取函数签名
            types = get_types_from_signature(signature)
            restype = signature.return_annotation  # 提取 argtypes 和 restype

            # 构建原型
            return cls(*types, restype=restype, name=name, signature=signature)

        if maybe_func is None:
            return decorator
        else:
            return decorator(maybe_func)
