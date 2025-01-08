import inspect
import types
import typing


def get_args(func):
    for i in inspect.signature(func).parameters.values():
        yield i


def get_name(func):
    return func.__name__


def get_doc(func):
    return func.__doc__


def get_code(func):
    return func.__code__


def get_source(func):
    return inspect.getsource(func)


def get_module(func):
    return func.__module__


def is_instance(ins_or_cls):
    return not isinstance(ins_or_cls, type)


def get_qualname(func_type_or_ins: typing.Union[types.FunctionType, type, object]):
    if is_instance(func_type_or_ins) and not is_function(func_type_or_ins):
        return get_qualname(func_type_or_ins.__class__)
    return f'{func_type_or_ins.__module__}.{func_type_or_ins.__qualname__}'


def is_function(obj):
    Func_Callable_Types = typing.Union[types.FunctionType, types.BuiltinFunctionType]
    return isinstance(obj, Func_Callable_Types)


class Function:
    def __init__(self, func):
        self._func = func
        self._signature = inspect.signature(func)

    @property
    def name(self):
        return get_name(self._func)

    @property
    def doc(self):
        return get_doc(self._func)

    @property
    def code(self):
        return get_code(self._func)

    @property
    def source(self):
        return get_source(self._func)

    @property
    def module(self):
        return get_module(self._func)

    @property
    def qualname(self):
        return get_qualname(self._func)

    @property
    def signature(self):
        return self._signature

    @property
    def params(self):
        return tuple(get_args(self._func))

    def match(self, *args, **kwargs):
        return self._signature.bind(*args, **kwargs)

    def __str__(self):
        return f'<Func {self.name} {self.qualname}>'

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)
