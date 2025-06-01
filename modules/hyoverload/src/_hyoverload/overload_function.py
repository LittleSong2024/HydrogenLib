from .errors import OverloadRuntimeError, OverloadError
from .namespace import _check_temp, get_func_overloads
from .type_checker import get_argtypes_degrees, get_signature_parameters_prec
from _hycore.type_func import Function, get_type_name


class OverloadFunction(Function):
    def __init__(self, func):
        super().__init__(func)
        self.params_dict = dict(self.signature.parameters)
        self.prec = get_signature_parameters_prec(self.signature)

    @property
    def callable(self):
        return OverloadFunctionCallable(self.qualname)

    def match(self, args, kwargs, instance=False):
        return get_argtypes_degrees(self.signature, args, kwargs, instance)

    def call(self, args, kwargs):
        try:
            return super().__call__(*args, **kwargs)
        except Exception as e:
            raise OverloadRuntimeError(self.qualname, self.signature, e, args, kwargs) from e

    def __lt__(self, other):
        return self.prec < other.prec

    def __eq__(self, other):
        return self.prec == other.prec

    def __gt__(self, other):
        return self.prec > other.prec

    def __str__(self):
        return f'{get_type_name(self)}{self.signature} with prec {self.prec}'

    __repr__ = __str__


class OverloadFunctionCallable:
    def __init__(self, qualname):
        self.qualname = qualname

    def call(self, args, kwargs, instance=False):
        # print("Args:", args, kwargs)
        if _check_temp(self.qualname, args):
            return

        results = []

        for func in get_func_overloads(self):
            prec = func.match(args, kwargs, instance)
            results.append((prec, func))

        prec, matched_func = max(results)

        if prec < 1:
            raise OverloadError(self.qualname, tuple(results), args, kwargs)

        return matched_func.call(args, kwargs)

    def __call__(self, *args, **kwargs):
        return self.call(args, kwargs)

    def __get__(self, instance, owner):
        # print('GET')
        return lambda *args, **kwargs: self.call((instance,) + args, kwargs, True)
