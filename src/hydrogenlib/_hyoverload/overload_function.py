import inspect
from fractions import Fraction
from inspect import signature, Signature

from .._hycore.type_func import get_qualname
from .._hycore.type_func import Function
from . import OverloadRuntimeError, OverloadError
from .namespace import _check_temp, get_func_overloads
from .type_checker import _get_match_degree, count_possible_types


class OverloadFunction:
    def __init__(self, func):
        self.func = Function(func)
        self.params = dict(self.signature.parameters)
        self.prec = get_prec(self.signature)
        self.is_method = inspect.ismethod(func)  # TODO: 无法正确识别方法函数

    @property
    def signature(self):
        return self.func.signature

    @property
    def qualname(self):
        return self.func.qualname

    def match(self, args, kwargs):
        if self.is_method:
            args = (None,) + args  # 针对方法函数，第一个参数为self, 进行参数绑定时应该加上
        return _get_match_degree(self.signature, args, kwargs)

    def call(self, args, kwargs):
        try:
            return self.func(*args, **kwargs)
        except Exception as e:
            raise OverloadRuntimeError(self.qualname, self.signature, e, args, kwargs)

    def __lt__(self, other):
        return self.prec < other.prec

    def __eq__(self, other):
        return self.prec == other.prec

    def __gt__(self, other):
        return self.prec > other.prec

    def __str__(self):
        return f'Overload({self.signature}) with prec {self.prec}'

    __repr__ = __str__


def get_prec(signature: Signature):
    return Fraction(
        sum(count_possible_types(param.annotation) for param in signature.parameters.values()),
        len(signature.parameters))


class OverloadFunctionCallable:
    def __init__(self, qualname):
        self.qualname = qualname

    def __call__(self, *args, **kwargs):
        print("Args:", args, kwargs)
        if _check_temp(self.qualname, args):
            return

        results = []

        for func in get_func_overloads(self.qualname):
            prec = func.match(args, kwargs)
            results.append((prec, func))

        prec, matched_func = max(results)

        if prec < 1:
            raise OverloadError(self.qualname, tuple(results), args, kwargs)

        return matched_func.call(args, kwargs)
