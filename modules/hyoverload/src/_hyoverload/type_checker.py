from fractions import Fraction
from inspect import Parameter, Signature, BoundArguments
from types import *
from typing import *

from .args_temp import Temp
from _hycore.typefunc import literal_eval


def get_typematch_degrees(argument, param_type):
    if isinstance(param_type, Parameter):
        param_type = param_type.annotation

    if isinstance(param_type, str):
        param_type = literal_eval(
            param_type,
            globals=globals(), locals=locals(), builtins=True, no_eval=False)

    origin = get_origin(param_type)

    if not isinstance(argument, param_type):  # 如果参数不匹配，则返回 0
        return 0

    if origin is Union:
        inner_types = get_args(param_type)
        matches = [get_typematch_degrees(argument, t) for t in inner_types]
        return sum(matches) / len(inner_types)

    elif origin in (List, Set, Deque, FrozenSet, Sequence):  # TODO: Not finished
        inner_types = get_args(param_type)
        if not inner_types:
            return 1  # No specific type specified, assume match
        inner_type = inner_types[0]
        return sum(
            get_typematch_degrees(item, inner_type) for item in inner_types) / len(inner_types) if argument else 1

    elif origin is Tuple:
        inner_types = get_args(param_type)

        if not inner_types:
            return 1  # No specific type specified, assume match

        if inner_types[-1] is Ellipsis:
            return sum(
                get_typematch_degrees(item, inner_types[0]) for item in argument)

        return sum(get_typematch_degrees(item, inner_type) for item, inner_type in zip(argument, inner_types)) / len(
            argument) if argument else 1

    elif origin is Dict:
        key_type, value_type = get_args(param_type)
        return sum(
            (get_typematch_degrees(value, value_type) + get_typematch_degrees(key, key_type)) / 2
            for key, value in argument.items()
        ) / len(argument) if argument else 1
    else:
        return 1 if isinstance(argument, param_type) else 0


def get_argtypes_degrees(signature: Signature, bound_args: BoundArguments, instance_method=False):
    if len(bound_args.arguments) == 0:
        return 1  # 如果没有参数，则一定是匹配的

    match_degrees = 0

    # for index, (param_name, arg) in enumerate(bound_args.arguments.items()):
    for param_name, arg in bound_args.arguments.items():
        param = signature.parameters[param_name]
        match_degrees += get_typematch_degrees(arg, param.annotation)

    length = len(bound_args.arguments)

    # print("Match Degrees:", match_degrees, "Length:", length)

    return match_degrees / length  # 匹配程度


def count_possible_types(type_hint):
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


def get_signature_parameters_prec(signature: Signature):
    return Fraction(
        sum(count_possible_types(param.annotation) for param in signature.parameters.values()),
        len(signature.parameters))


class SignatureMatcher:
    def __init__(self, signature: Signature):
        self._signature = signature
        self._signature_prec = get_signature_parameters_prec(self._signature)

    @property
    def signature(self):
        return self._signature

    def get_calling_degrees(self, args, kwargs):
        try:
            bound_args = self._signature.bind(*args, **kwargs)
        except TypeError as e:
            return -1

        return get_argtypes_degrees(self._signature)


class MultiSignatureMatcher:
    def __init__(self, signatures: List[Signature], temp=None):
        self._signatures = signatures
        self._matchers = [SignatureMatcher(sig) for sig in signatures]
        self._temp = temp or Temp()

    def match(self, args, kwargs) -> List[SignatureMatcher]:
        ls = [
            (matcher.get_calling_degrees(args, kwargs), matcher) for matcher in self._matchers]
        ls.sort(reverse=True)
        return [matcher for _, matcher in ls]

    def add(self, signature):
        matcher = SignatureMatcher(signature)

        self._signatures.append(signature)
        self._matchers.append(matcher)

        return matcher
