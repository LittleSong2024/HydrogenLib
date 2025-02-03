import sys
from fractions import Fraction
from inspect import signature, Signature, Parameter
from types import UnionType
from typing import *

import rich.traceback

from ..Func import *
from ...data_structures import Heap
from ..LiteralEval import literal_eval

overloads = {}  # type: dict[str, Heap]
overload_temp = {}  # type: dict[str, dict[tuple[type, ...], OverloadFunctionCallable]]
overload_funcs = {}  # type: dict[str, OverloadFunctionCallable]


# TODO: 完成模块

def _register(qual_name, func: 'OverloadFunction'):
    if qual_name not in overload_funcs:
        overload_funcs[qual_name] = OverloadFunctionCallable(qual_name)
    return _get_registered(qual_name)


def _get_registered(qual_name):
    return overload_funcs[qual_name]


def _add_to_temp(qual_name, types):
    if qual_name not in overload_temp:
        overload_temp[qual_name] = dict()
    overload_temp[qual_name][types] = _get_registered(qual_name)


def _check_temp(qual_name, args):
    if qual_name not in overload_temp:
        return False
    for types in overload_temp[qual_name]:
        if len(types) != len(args):
            continue
        for arg, type_ in zip(args, types):
            if not isinstance(arg, type_):
                return False


def _match_type(arg, param_type):
    if isinstance(param_type, Parameter):
        param_type = param_type.annotation

    if isinstance(param_type, str):
        param_type = literal_eval(param_type, globals=globals(), locals=locals(), builtins=True, no_eval=False)

    origin = get_origin(param_type)

    if origin is Union:
        types = get_args(param_type)
        matches = [_match_type(arg, t) for t in types]
        return sum(matches) / len(types)

    elif origin in (List, Set, Deque, FrozenSet, Sequence):  # TODO: Not finished
        inner_types = get_args(param_type)
        if not inner_types:
            return 1  # No specific type specified, assume match
        inner_type = inner_types[0]
        if isinstance(arg, origin):  # 如果arg是序列类型之一
            return sum(_match_type(item, inner_type) for item in arg) / len(arg) if arg else 1
        else:
            return 0

    elif origin is Tuple:
        inner_types = get_args(param_type)
        if not inner_types:
            return 1  # No specific type specified, assume match
        if isinstance(arg, tuple):  # 如果arg是元组
            return sum(_match_type(item, inner_type) for item, inner_type in zip(arg, inner_types)) / len(
                arg) if arg else 1
        else:
            return 0

    elif origin is Dict:
        kt, vt = get_args(param_type)
        if isinstance(arg, dict):  # 如果arg是字典
            return sum(
                (_match_type(v, vt) + _match_type(k, kt)) / 2
                for k, v in arg.items()) / len(arg) if arg else 1
        else:
            return 0
    else:
        return 1 if isinstance(arg, param_type) else 0


def _get_match_degree(signature: Signature, args):
    match_degrees = []
    bound_args = signature.bind(*args)
    for param_name, arg in bound_args.arguments.items():
        param = signature.parameters[param_name]
        match_degrees.append(_match_type(arg, param.annotation))

    return sum(match_degrees) / len(match_degrees) if match_degrees else 0  # 匹配程度


def count_possible_types(type_hint):
    # if type_hint is type:
    #     return 1
    print("Type:", type_hint)
    origin = get_origin(type_hint)
    if origin in (Union, UnionType):
        # 如果是Union类型，递归计算每个成员的可能类型数量
        return sum(count_possible_types(arg) for arg in get_args(type_hint))
    elif origin is List:
        # 如果是List类型，递归计算元素类型的可能类型数量
        element_type = get_args(type_hint)[0]
        return count_possible_types(element_type)
    elif origin is Tuple:
        # 如果是Tuple类型，递归计算每个元素类型的可能类型数量
        return sum(count_possible_types(arg) for arg in get_args(type_hint))
    elif origin is Optional:
        # 如果是Optional类型，递归计算内部类型的可能类型数量，并加上None
        return count_possible_types(get_args(type_hint)[0]) + 1
    else:
        # 基本类型或其他类型，返回1
        return 1


class ErrorDecorater:
    def __init__(self, exc):
        self.exception = exc

    def __bool__(self):
        return False

    def __str__(self):
        return str(self.exception)

    __repr__ = __str__


class OverloadError(Exception):
    def __init__(self, qual_name, tests=(), args=(), kwargs=None):
        self.qual_name = qual_name
        self.tests = tests
        self.msg = ''
        self.args = args
        self.kwargs = kwargs if kwargs else {}

    @staticmethod
    def to_call_format(args, kwargs):
        string = ', '.join(
            list(map(lambda x: type(x).__name__, args)) +
            list(map(lambda x: f'{x[0]}={type(x[1]).__name__}', kwargs.items()))
        )
        return string

    @staticmethod
    def to_args_format(signature: Signature):
        params = signature.parameters
        string = ', '.join(
            list(map(str, params.values()))
        )
        return string

    @staticmethod
    def to_type_name(type_: inspect.Parameter):
        if type_.annotation is inspect.Parameter.empty:
            return 'Any'
        else:
            return str(type_.annotation.__name__)

    @staticmethod
    def __rich_to_string(string):
        console = rich.get_console()
        rich_string = console.render(string)
        result = ''
        for part in rich_string:
            result += str(part.text)
        return result

    def __generate_error_msg(self):
        error_msg = ''

        def add_error_msg(string):
            nonlocal error_msg
            error_msg += self.__rich_to_string(string)

        add_error_msg(f'[red]调用{self.qual_name}时发生错误: 无法匹配重载类型[/red]')
        add_error_msg(f'[yellow]传入的实参:[/yellow] {self.to_call_format(self.args, self.kwargs)}')
        for test, func in zip(self.tests, overloads[self.qual_name]):
            add_error_msg(
                f'\t[yellow]尝试匹配: {func.signature} [/yellow]'
                f'[red]: {str(test)}[/red]'
            )
        return error_msg

    def __str__(self):
        try:
            return self.__generate_error_msg()
        except Exception as e:
            return str(e)


class OverloadRuntimeError(Exception):
    def __init__(self, qualname, called_overload, e, call_args, call_kwargs):
        self.qualname = qualname
        self.called_overload = called_overload
        self.e = e
        self.call_args = call_args
        self.call_kwargs = call_kwargs

    def __str__(self):
        return (f'\n\t以参数({OverloadError.to_call_format(self.call_args, self.call_kwargs)})'
                f'调用`{self.qualname}`'
                f'的重载 "{self.called_overload}" '
                f'时发生错误.'
                f'\n\t详细信息 {self.e.__class__.__name__}: {self.e}'
                )


def _get_module_globals(module_name):
    try:
        module = sys.modules[module_name]
        return module.__dict__
    except KeyError:
        return {}


class OverloadFunction:
    def __init__(self, func):
        self.func = func
        self.qual_name = get_qualname(func)
        self.signature = signature(func)
        self.params = dict(self.signature.parameters)
        self.prec = self.get_prec(self.signature)
        # print("重载精确度:", self.prec)

    @staticmethod
    def get_prec(signature: Signature):
        return Fraction(
            sum(count_possible_types(param.annotation) for param in signature.parameters.values()),
            len(signature.parameters))

    def __lt__(self, other):
        return self.prec < other.prec

    def __eq__(self, other):
        return self.prec == other.prec

    def __gt__(self, other):
        return self.prec > other.prec

    def __str__(self):
        return f'Overload({self.signature}) with prec {self.prec}'

    __repr__ = __str__


class OverloadFunctionCallable:
    def __init__(self, qualname):
        self.qualname = qualname

    def _call(self, func: OverloadFunction, args, kwargs):
        try:
            return func.func(*args, **kwargs)
        except Exception as e:
            raise OverloadRuntimeError(self.qualname, func.signature, e, args, kwargs)

    def __call__(self, *args, **kwargs):
        if _check_temp(self.qualname, args):
            return
        res_ls = []
        func: OverloadFunction
        for func in overloads[self.qualname]:
            res = _get_match_degree(func.signature, args)
            res_ls.append((res, func))

        res, matched_func = max(res_ls)
        if res < 1:
            raise OverloadError(self.qualname, tuple(res_ls), args, kwargs)

        return self._call(matched_func, args, kwargs)


def overload(func):
    func = OverloadFunction(func)
    if func.qual_name in overloads:
        overloads[func.qual_name].append(func)
    else:
        overloads[func.qual_name] = Heap([func], True)

    return _register(func.qual_name, func)


def get_func_overloads(func: OverloadFunctionCallable):
    return overloads[func.qualname]
