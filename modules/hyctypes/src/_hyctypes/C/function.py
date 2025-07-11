from inspect import Signature, Parameter

from _hycore.utils import InstanceDict
from .prototype import ProtoType
from .basic_types import convert_cdata, as_cdata


class WrapedArguments:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def call(self, func):
        return func(*self.args, **self.kwargs)


class Function:
    _methods = InstanceDict()

    def __init__(self, prototype: ProtoType, signature: Signature = None, dll=None):
        self._name = prototype.name
        self._dll = dll
        self._prototype = prototype
        self._signature = signature or Signature(  # 生成 signature 来方便类型检查
            [
                Parameter(f'Arg_{index}', Parameter.POSITIONAL_OR_KEYWORD, annotation=tp)
                for index, tp in zip(
                range(len(self._prototype.argtypes)),
                self._prototype.argtypes
            )
            ],
            return_annotation=self._prototype.restype
        )

        self._lz_fpointer = None  # 懒加载
        # DLLPointer 实际既可以表示函数指针,又可以表示变量指针,这里我们将它作为函数指针使用

    @property
    def func_ptr(self):
        if self._lz_fpointer is None:
            if self._dll is None or not self._dll.ready():
                raise RuntimeError('dll is not ready')
            self._lz_fpointer = self._dll.addr(self._name)
        return self._lz_fpointer

    @classmethod
    def define(cls, maybe_func=None, *, name: str = None, dll=None):
        def decorator(func):
            prototype = ProtoType.from_pyfunc(func, name)
            fnc = cls(prototype, dll=dll, signature=prototype.py_signature)
            return fnc

        if maybe_func is None:
            return decorator
        else:
            return decorator(maybe_func)

    @classmethod
    def wrap(cls, maybe_func=None, *, name: str = None, dll=None, real_prototype=None):
        def decorator(func):
            prototype = real_prototype or ProtoType.from_pyfunc(func, name=name)
            prototype.name = prototype.name or name
            fnc = cls(prototype, dll=dll, signature=prototype.py_signature)

            def wrapper(*args, **kwargs):
                arguments = func(*args, **kwargs)  # type: WrapedArguments
                if not isinstance(arguments, WrapedArguments):
                    # 必须返回 WrapedArguments
                    raise TypeError("return must be WrapedArguments")
                return arguments.call(fnc)

            return wrapper

        if maybe_func is None:
            return decorator
        else:
            return decorator(maybe_func)

    def convert_args(self, args, kwargs):
        bound_args = self._signature.bind(*args, **kwargs).arguments.values()
        for tp, arg in zip(self._prototype.argtypes, bound_args):
            try:
                yield as_cdata(convert_cdata(arg, tp))
            except TypeError as e:
                raise TypeError(str(e))

    def set_source(self, dll):
        if self._dll is not None:
            raise TypeError('dll is already set')
        self._dll = dll

    def __call__(self, *args, **kwargs):
        return self.func_ptr(*self.convert_args(args, kwargs))  # 不要用 kwargs

    def __get__(self, inst, cls):
        if inst in self._methods:
            return self._methods[inst]
        else:
            self._methods[inst] = Method(inst, self)
            return self._methods[inst]


class Method:
    __self__ = None

    def __init__(self, inst, func: Function):
        self.__self__ = inst
        self.__func__ = func

    def __call__(self, *args, **kwargs):
        return self.__func__(self.__self__, *args, **kwargs)
