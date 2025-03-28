import inspect
import types
import typing
from inspect import stack as call_stack

from .list_func import hasindex


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


def get_module(func) -> str:
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


def get_signature(func):
    return inspect.signature(func)


class Function:
    def __init__(self, func):
        if isinstance(func, self.__class__):
            self._func = func._func
        else:
            self._func = func

        self._signature = None

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
        if not self._signature:
            self._signature = inspect.signature(self._func)
        return self._signature

    @property
    def params(self):
        return tuple(get_args(self._func))

    def match(self, *args, **kwargs):
        return self._signature.bind(*args, **kwargs)

    def __str__(self):
        return f'<Func {self.qualname} ({self._signature})>'

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)


class FunctionGroup:
    def __init__(self, funcs: typing.Iterable):
        self._funcs = list(funcs)

    def __iter__(self):
        return iter(self._funcs)

    def __len__(self):
        return len(self._funcs)

    def __getitem__(self, item):
        return self._funcs[item]

    def __setitem__(self, key, value):
        self._funcs[key] = value

    def __delitem__(self, key):
        del self._funcs[key]

    def __contains__(self, item):
        return item in self._funcs

    def __call__(self, *args, **kwargs):
        for func in self._funcs:
            func(*args, **kwargs)

    def __add__(self, other):
        if isinstance(other, type(self)):
            return type(self)(self._funcs + other._funcs)
        elif isinstance(other, typing.Callable):
            return type(self)(self._funcs + [other])

    def __iadd__(self, other):
        if isinstance(other, type(self)):
            self._funcs += other._funcs
            return self


def get_called_func(depth=1):
    call_stck = call_stack()
    if not hasindex(call_stck, depth):
        return None
    return call_stck[depth].frame.f_code.co_qualname
