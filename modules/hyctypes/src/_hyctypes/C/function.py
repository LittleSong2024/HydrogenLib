from inspect import Signature, Parameter

from _hycore.utils import InstanceDict
from .dll_pointer import DLLPointer
from .prototype import ProtoType
from .methods import type_convert

from . import type_hints as th


class Function:
    _instance_dict = InstanceDict()

    def __init__(self, prototype: ProtoType, signature: Signature = None, dll=None):
        self._name = prototype.name
        self._dll = dll
        self._prototype = prototype
        self._signature = signature or Signature(  # 生成 signature 来方便类型检查
            [
                Parameter(f'arg_{index}', Parameter.POSITIONAL_OR_KEYWORD, annotation=tp)
                for index, tp in zip(
                range(len(self._prototype.argtypes)),
                self._prototype.argtypes
            )
            ],
            return_annotation=self._prototype.restype
        )

        self.__fpointer = None  # 懒加载
        # DLLPointer 实际既可以表示函数指针,又可以表示变量指针,这里我们将它作为函数指针使用

    @property
    def _fpointer(self):
        if self.__fpointer is None:
            if self._dll is None or not self._dll.ready():
                raise RuntimeError('dll is not ready')
            self.__fpointer = self._dll.addr(self._name)
        return self.__fpointer

    @classmethod
    def define(cls, maybe_func=None, *, name: str = None, dll=None):
        def decorator(func):
            prototype = ProtoType.from_pyfunc(func, name)
            fnc = cls(prototype, dll=dll)
            return fnc

        if maybe_func is None:
            return decorator
        else:
            return decorator(maybe_func)

    def __type_check(self, args, kwargs):
        bound_args = self._signature.bind(*args, **kwargs).arguments.values()
        final_args = []
        for tp, arg in zip(self._prototype.argtypes, bound_args):
            try:
                final_args.append(type_convert(arg, tp))
            except TypeError as e:
                raise TypeError(str(e)) from None
        return final_args

    def set_source(self, dll):
        if self._dll is not None:
            raise TypeError('dll is already set')
        self._dll = dll

    def __call__(self, *args, **kwargs):
        args = self.__type_check(args, kwargs)
        return self._fpointer(*args)  # 不要用 kwargs

    def __get__(self, inst, cls):
        if inst in self._instance_dict:
            return self._instance_dict[inst]
        else:
            self._instance_dict[inst] = Method(inst, self)
            return self._instance_dict[inst]


class Method:
    __self__ = None

    def __init__(self, inst, func: Function):
        self.__self__ = inst
        self.__func__ = func

    def __call__(self, *args, **kwargs):
        return self.__func__(self.__self__, *args, **kwargs)
